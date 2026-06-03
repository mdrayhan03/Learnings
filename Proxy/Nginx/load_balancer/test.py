"""
Load-test the NGINX load balancer at http://localhost:80.

Spawns N worker threads that hammer the proxy in a loop, prints a live
ticker (throughput, status codes, errors, per-backend distribution) every
second, and polls `docker stats` + `docker inspect` so you can SEE
containers die, get OOMKilled, and restart in real time.

Usage:
    python test.py                                          # quick smoke test
    python test.py --endpoint /crash --workers 50 --duration 30
    python test.py --endpoint /crash --workers 100 --duration 60 --timeout 10
"""

import argparse
import collections
import json
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


TARGET = "http://localhost:80"
BACKEND_RE = re.compile(r"app\s*(\d+)", re.IGNORECASE)

# Shared counters (protected by `lock`)
counts = collections.Counter()                    # backend -> request count
status_counts = collections.Counter()             # http status -> count
status_by_backend = collections.defaultdict(collections.Counter)  # backend -> status -> count
pids_seen = collections.defaultdict(set)          # backend -> {pid, pid, ...} (>1 = restarted)
errors = collections.Counter()                    # exception class -> count
latencies = []
recent_window = collections.deque()               # (timestamp, status_or_error) for live ticker
lock = threading.Lock()
stop_flag = threading.Event()
START = 0.0


def make_session():
    s = requests.Session()
    adapter = HTTPAdapter(
        pool_connections=200,
        pool_maxsize=200,
        max_retries=Retry(total=0),   # surface every failure, don't hide it
    )
    s.mount("http://", adapter)
    return s


def identify_backend(text: str):
    """Return (backend_name, pid_or_None). Handles both JSON (/crash) and plain text (/)."""
    pid = None
    backend = None
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "app" in data:
            backend = f"app_{data['app']}"
            pid = data.get("pid")
    except (ValueError, TypeError):
        pass

    if backend is None:
        m = BACKEND_RE.search(text or "")
        if m:
            backend = f"app_{m.group(1)}"

    return backend or "unknown", pid


def worker(endpoint: str, timeout: float):
    session = make_session()
    while not stop_flag.is_set():
        t0 = time.perf_counter()
        try:
            r = session.get(TARGET + endpoint, timeout=timeout)
            dt = time.perf_counter() - t0
            backend, pid = identify_backend(r.text)
            now = time.time()
            with lock:
                status_counts[r.status_code] += 1
                status_by_backend[backend][r.status_code] += 1
                latencies.append(dt)
                counts[backend] += 1
                if pid is not None:
                    pids_seen[backend].add(pid)
                recent_window.append((now, r.status_code))
        except requests.RequestException as e:
            now = time.time()
            with lock:
                err_name = type(e).__name__
                errors[err_name] += 1
                recent_window.append((now, err_name))


def live_ticker(interval: float):
    """Print throughput / status snapshot every `interval` seconds."""
    last_total = 0
    while not stop_flag.is_set():
        time.sleep(interval)
        with lock:
            total = sum(status_counts.values()) + sum(errors.values())
            # Trim window to last 5s
            cutoff = time.time() - 5
            while recent_window and recent_window[0][0] < cutoff:
                recent_window.popleft()
            recent_2xx = sum(1 for _, s in recent_window if isinstance(s, int) and 200 <= s < 300)
            recent_5xx = sum(1 for _, s in recent_window if isinstance(s, int) and 500 <= s < 600)
            recent_err = sum(1 for _, s in recent_window if not isinstance(s, int))
            recent_total = len(recent_window)
            per_backend = dict(counts)

        rps = (total - last_total) / interval
        last_total = total
        elapsed = time.time() - START

        flag = ""
        if recent_5xx or recent_err:
            flag = "  <-- backends struggling!"

        line = (
            f"[t={elapsed:5.1f}s] total={total:6d}  rps={rps:6.1f}  "
            f"(last 5s: 2xx={recent_2xx} 5xx={recent_5xx} err={recent_err} of {recent_total})"
            f"{flag}"
        )
        print(line)
        if per_backend:
            dist = "  backends: " + "  ".join(
                f"{k}={v}" for k, v in sorted(per_backend.items())
            )
            print(dist)


def stats_monitor(interval: float):
    """Poll `docker stats` once per `interval` seconds and print a snapshot."""
    while not stop_flag.is_set():
        try:
            out = subprocess.check_output(
                [
                    "docker", "stats", "--no-stream", "--format",
                    "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"[stats] docker not available: {e}")
            return

        rows = [r for r in out.strip().splitlines() if "flask_app" in r or "nginx" in r]
        if rows:
            print(f"\n--- docker stats @ {time.time() - START:.1f}s ---")
            print(f"{'NAME':<42} {'CPU%':>8}   {'MEM':<24} {'MEM%':>7}")
            for row in rows:
                name, cpu, mem, mem_pct = row.split("\t")
                print(f"{name:<42} {cpu:>8}   {mem:<24} {mem_pct:>7}")
            print()

        for _ in range(int(interval * 10)):
            if stop_flag.is_set():
                return
            time.sleep(0.1)


def inspect_containers():
    """Return per-container {OOMKilled, ExitCode, RestartCount, Status} after the test."""
    try:
        ids_out = subprocess.check_output(
            ["docker", "ps", "-a", "--format", "{{.ID}}\t{{.Names}}"],
            text=True, stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}

    result = {}
    for line in ids_out.strip().splitlines():
        cid, name = line.split("\t", 1)
        if "flask_app" not in name and "nginx" not in name:
            continue
        try:
            raw = subprocess.check_output(
                ["docker", "inspect", cid], text=True, stderr=subprocess.DEVNULL,
            )
            data = json.loads(raw)[0]
            state = data.get("State", {})
            result[name] = {
                "Status": state.get("Status"),
                "OOMKilled": state.get("OOMKilled"),
                "ExitCode": state.get("ExitCode"),
                "RestartCount": data.get("RestartCount", 0),
            }
        except (subprocess.CalledProcessError, ValueError, KeyError, IndexError):
            continue
    return result


def percentile(values, p):
    if not values:
        return 0.0
    values = sorted(values)
    k = max(0, min(len(values) - 1, int(round((p / 100) * (len(values) - 1)))))
    return values[k]


def print_summary(elapsed: float):
    total = sum(status_counts.values())
    err_total = sum(errors.values())
    print("\n" + "=" * 72)
    print("ATTACK SUMMARY")
    print("=" * 72)
    print(f"Duration:        {elapsed:.2f}s")
    print(f"Total responses: {total}")
    print(f"Throughput:      {total / elapsed:.1f} req/s")
    print(f"Errors:          {err_total}")

    if latencies:
        print("\nLatency (ms):")
        print(f"  p50 = {percentile(latencies, 50) * 1000:.1f}")
        print(f"  p95 = {percentile(latencies, 95) * 1000:.1f}")
        print(f"  p99 = {percentile(latencies, 99) * 1000:.1f}")
        print(f"  max = {max(latencies) * 1000:.1f}")

    print("\nBackend distribution + status breakdown:")
    print(f"  {'backend':<10} {'total':>8} {'pids_seen':>10}   status codes")
    for k in sorted(counts):
        pids = pids_seen.get(k, set())
        status_str = "  ".join(f"{s}:{v}" for s, v in sorted(status_by_backend[k].items()))
        flag = "  <-- RESTARTED" if len(pids) > 1 else ""
        print(f"  {k:<10} {counts[k]:>8} {len(pids):>10}   {status_str}{flag}")

    print("\nHTTP status codes (overall):")
    for k, v in sorted(status_counts.items()):
        note = ""
        if k == 502:
            note = "  (Bad Gateway -- nginx couldn't reach upstream; backend likely dead)"
        elif k == 504:
            note = "  (Gateway Timeout -- upstream too slow)"
        elif k == 503:
            note = "  (Service Unavailable -- nginx out of upstream slots)"
        print(f"  {k}  {v}{note}")

    if errors:
        print("\nClient-side errors:")
        for k, v in errors.most_common():
            print(f"  {k:<30} {v}")

    print("\nContainer post-mortem (`docker inspect`):")
    info = inspect_containers()
    if not info:
        print("  (could not inspect — is docker running?)")
    else:
        any_oom = False
        for name in sorted(info):
            s = info[name]
            flag = ""
            if s["OOMKilled"]:
                flag = "  <-- OOMKilled !!!"
                any_oom = True
            elif s["RestartCount"]:
                flag = f"  <-- restarted {s['RestartCount']}x"
            print(
                f"  {name:<42}  status={s['Status']:<10} "
                f"exit={s['ExitCode']}  restarts={s['RestartCount']}  "
                f"OOMKilled={s['OOMKilled']}{flag}"
            )
        if any_oom:
            print("\n  CRASH ROOT CAUSE: container exceeded mem_limit -> kernel OOM-killer fired.")
            print("  Exit code 137 = 128 + SIGKILL(9). Confirm: `docker compose logs <svc>`.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=50)
    ap.add_argument("--duration", type=int, default=30)
    ap.add_argument("--endpoint", default="/crash")
    ap.add_argument("--timeout", type=float, default=10.0,
                    help="per-request timeout in seconds (default: 10)")
    ap.add_argument("--ticker-interval", type=float, default=1.0)
    ap.add_argument("--stats-interval", type=float, default=3.0)
    args = ap.parse_args()

    print(f"Hammering {TARGET}{args.endpoint}")
    print(f"  workers={args.workers}  duration={args.duration}s  timeout={args.timeout}s")
    print("Ctrl-C to stop early.\n")

    global START
    START = time.time()

    threading.Thread(target=live_ticker, args=(args.ticker_interval,), daemon=True).start()
    threading.Thread(target=stats_monitor, args=(args.stats_interval,), daemon=True).start()

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for _ in range(args.workers):
                pool.submit(worker, args.endpoint, args.timeout)
            time.sleep(args.duration)
            stop_flag.set()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        stop_flag.set()

    elapsed = time.time() - START
    print_summary(elapsed)


if __name__ == "__main__":
    sys.exit(main())
