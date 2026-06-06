import os
import time
import threading
from flask import Flask, request, jsonify

APP_ID = 1

app = Flask(__name__)

# Module-global list = permanent memory leak (never garbage collected).
# Every /crash request appends a chunk here, so RSS grows monotonically
# until the kernel OOM-kills the container.
LEAK = []
LEAK_LOCK = threading.Lock()


@app.route('/')
def home():
    return f"Hello I am app {APP_ID} from behind the secure NGINX proxy!"


@app.route('/headers')
def headers():
    return jsonify(dict(request.headers))


@app.route('/healthz')
def healthz():
    # Cheap endpoint that does NOT touch LEAK — useful to check liveness
    # while /crash hammers the container.
    return jsonify(status="ok", app=APP_ID, pid=os.getpid(), leaked_mb=_leaked_mb())


@app.route('/crash')
def crash():
    """
    Simulates a real-world bad endpoint:
      1. Permanently leaks ~30MB of RAM per request (memory pressure -> OOMKilled)
      2. Burns CPU for ~0.3s   (CPU saturation -> queueing -> high p99)
      3. Sleeps  for ~1.0s     (I/O wait -> nginx upstream queue fills up -> 502/504)
    With mem_limit=200m and 30MB leaked per request, each container dies
    after roughly 5-6 successful hits.
    """
    # 1. Memory leak: 30MB, held forever
    chunk = bytearray(30 * 1024 * 1024)  # touches pages -> real RSS, not lazy
    with LEAK_LOCK:
        LEAK.append(chunk)

    # 2. CPU burn
    t_end = time.perf_counter() + 0.3
    x = 0
    while time.perf_counter() < t_end:
        x += sum(i * i for i in range(500))

    # 3. Slow downstream simulation
    time.sleep(1.0)

    return jsonify(
        app=APP_ID,
        pid=os.getpid(),
        leaked_mb=_leaked_mb(),
        msg=f"app {APP_ID} survived... for now",
    )


def _leaked_mb():
    with LEAK_LOCK:
        return sum(len(c) for c in LEAK) // (1024 * 1024)


if __name__ == '__main__':
    # threaded=True so multiple requests run concurrently inside one container
    # -> memory + CPU pressure compound, exactly like a real prod incident.
    app.run(host='0.0.0.0', port=5000, threaded=True)
