import threading
import time
import random
import queue

class BoundedThreadPool:
    def __init__(self, num_threads: int, max_queue_size: int):
        self.max_queue_size = max_queue_size
        
        # Core Bounded Buffer
        self.task_queue = queue.Queue(maxsize=max_queue_size)
        self.workers = []
        self.is_shutdown = False

        # Spawn the static, long-lived worker pool threads immediately
        print(f"🏗️  [POOL INIT] Spawning {num_threads} static worker threads...")
        for i in range(1, num_threads + 1):
            t = threading.Thread(
                target=self._worker_loop, 
                args=(f"PoolWorker-{i}",), 
                daemon=True # Allows the system to exit cleanly when main ends
            )
            self.workers.append(t)
            t.start()

    def submit_task(self, task_func, *args):
        """Submits a task to the queue, or executes the Caller-Runs fallback if full."""
        if self.is_shutdown:
            raise RuntimeError("Cannot submit tasks to a shut down pool.")

        task_payload = (task_func, args)

        try:
            # Attempt a non-blocking queue insertion
            self.task_queue.put_nowait(task_payload)
            
        except queue.Full:
            # 🚨 CALLER-RUNS BACKPRESSURE REJECTION POLICY
            # The current thread (the main ingestion thread) executes the task itself!
            caller_name = threading.current_thread().name
            print(f"⚠️  [BACKPRESSURE] Queue full ({self.task_queue.qsize()} items). {caller_name} is forced to run task directly!")
            
            # Execute synchronously on the calling thread's stack frame
            task_func(*args)

    def _worker_loop(self, worker_name: str):
        """The permanent loop executed by background threads pulling work tasks."""
        while True:
            # Block and wait for a task to drop into the buffer
            task = self.task_queue.get()
            
            # Poison Pill pattern for graceful shutdowns
            if task is None:
                self.task_queue.task_done()
                break
                
            task_func, task_args = task
            # Run the task within the isolated background worker context
            task_func(worker_name, *task_args)
            
            # Signal task completion to the queue engine
            self.task_queue.task_done()

    def wait_and_shutdown(self):
        """Gracefully drains the active queue and terminates background workers."""
        print("\n🛑 [SHUTDOWN] Initiating pool drain pipeline...")
        self.is_shutdown = True
        
        # Block main thread execution until the queue is completely empty
        self.task_queue.join()
        
        # Inject "Poison Pills" to stop the infinite worker loops safely
        for _ in self.workers:
            self.task_queue.put(None)
            
        for t in self.workers:
            t.join()
        print("✅ [SHUTDOWN] Thread pool completely terminated.")


# --- Simulation Task & Runner Configuration ---
def parse_and_process_log(executing_thread_name: str, log_id: int):
    """The simulated CPU/IO heavy logging execution task payload"""
    # Simulate processing work latency
    time.sleep(random.uniform(0.01, 0.03))
    print(f"💾 [LOG-PROCESSED] Thread [{executing_thread_name}] parsed Event ID: {log_id}")


if __name__ == "__main__":
    # Max Threads: 3 | Max Backlog Capacity Queue Size: 10
    pool = BoundedThreadPool(num_threads=3, max_queue_size=10)

    print("\n🚀 [START] Simulating a sudden massive burst of 50 log events...")
    
    # The main thread acts as the high-throughput ingestion hook
    for i in range(1, 51):
        pool.submit_task(parse_and_process_log, i)
        # Simulate highly rapid log arrivals
        time.sleep(0.002)

    # Clean up and gracefully terminate the process
    pool.wait_and_shutdown()