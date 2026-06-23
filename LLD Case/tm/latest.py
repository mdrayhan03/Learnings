import threading
import time
import random

class RateLimitedConnectionPool:
    def __init__(self, max_capacity=3):
        self.max_capacity = max_capacity
        
        # Absolute Source of Truth: Shared resource tracking array
        self._pool = [f"Conn-Socket-{i}" for i in range(1, max_capacity + 1)]
        
        # Primitive A: The Counting Semaphore handles multi-threaded throttling/signaling
        self._semaphore = threading.Semaphore(max_capacity)
        
        # Primitive B: Standard Mutex protects the internal list structure from race conditions
        self._list_lock = threading.Lock()

    def get_connection(self, worker_id: str) -> str:
        """
        Fetches an available database socket. If the pool is exhausted, 
        the calling thread is safely suspended until a resource is returned.
        """
        # 1. Acquire the Semaphore. If count is 0, this thread sleeps automatically.
        self._semaphore.acquire()
        
        # 2. Critical Section: Safely mutate the shared pool array under a Mutex Lock
        with self._list_lock:
            connection = self._pool.pop(0)
            print(f"🔌 [CHECKOUT] {worker_id} grabbed {connection}. Available Slots left: {len(self._pool)}")
            
        return connection

    def release_connection(self, connection: str, worker_id: str):
        """
        Returns a socket back to the shared pool and signals the next 
        waiting thread to wake up.
        """
        # 1. Critical Section: Safely return the resource back to the array structure
        with self._list_lock:
            self._pool.append(connection)
            print(f"♻️ [RETURN]   {worker_id} returned {connection}. Available Slots left: {len(self._pool)}")
            
        # 2. Increment semaphore and wake up the next suspended thread in line
        self._semaphore.release()


# --- Simulation Runner Configuration ---
def worker_task(worker_name: str, pool: RateLimitedConnectionPool):
    print(f"📡 [REQUEST]  {worker_name} is requesting a connection socket...")
    
    # Block/Sleep happens right inside here if capacity is reached
    conn = pool.get_connection(worker_name)
    
    # Simulate active database processing runtime latency
    time.sleep(random.uniform(0.2, 0.4)) 
    
    pool.release_connection(conn, worker_name)


if __name__ == "__main__":
    # Initialize connection cap to 3
    connection_pool = RateLimitedConnectionPool(max_capacity=3)
    worker_threads = []

    print("--- Starting Rate-Limited Connection Pool Simulation ---")
    print("Pool Cap: 3 | Total Workers: 15 (No busy-waiting spin loops!)\n")

    # Spawn 15 concurrent workers attacking a pool capped at 3
    for i in range(1, 16):
        t = threading.Thread(target=worker_task, args=(f"Worker-{i}", connection_pool))
        worker_threads.append(t)
        t.start()

    # Block main thread execution until all workers complete
    for t in worker_threads:
        t.join()

    print("\n✅ Simulation Complete. All threads synchronized and allocated seamlessly.")