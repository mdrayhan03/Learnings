import os
import time
import threading
from flask import Flask, request, jsonify

APP_ID = 2

app = Flask(__name__)

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
    return jsonify(status="ok", app=APP_ID, pid=os.getpid(), leaked_mb=_leaked_mb())


@app.route('/crash')
def crash():
    chunk = bytearray(30 * 1024 * 1024)
    with LEAK_LOCK:
        LEAK.append(chunk)

    t_end = time.perf_counter() + 0.3
    x = 0
    while time.perf_counter() < t_end:
        x += sum(i * i for i in range(500))

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
    app.run(host='0.0.0.0', port=5000, threaded=True)
