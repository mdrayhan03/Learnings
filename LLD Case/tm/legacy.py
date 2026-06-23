import threading
import time
import random

class NaiveConnectionPool:
    def __init__(self, max_capacity=3):
        self.max_capacity = max_capacity
        # Simulate physical connection strings or sockets
        self.pool = [f"Conn-Socket-{i}" for i in range(1, max_capacity + 1)]

    def get_connection(self, worker_id):
        # ⚠️ CRITICAL FLAW: CPU Busy-Waiting Spin Loop!
        # This wastes millions of CPU cycles while waiting for a free connection
        while len(self.pool) == 0:
            pass  # Spinning infinitely
            
        conn = self.pool.pop(0)
        print(f"🔌 [CHECKOUT] {worker_id} grabbed {conn}. Remaining: {len(self.pool)}")
        return conn

    def release_connection(self, conn, worker_id):
        self.pool.append(conn)
        print(f"♻️ [RETURN] {worker_id} returned {conn}. Remaining: {len(self.pool)}")

# --- Simulation Setup ---
pool_engine = NaiveConnectionPool(max_capacity=3)

def worker_task(worker_name):
    conn = pool_engine.get_connection(worker_name)
    time.sleep(random.uniform(0.1, 0.3)) # Simulate doing database queries
    pool_engine.release_connection(conn, worker_name)

# 15 concurrent workers attacking a pool of size 3
for i in range(1, 16):
    threading.Thread(target=worker_task, args=(f"Worker-{i}",)).start()