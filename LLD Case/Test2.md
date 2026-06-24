# 🏛️ Junior Software Engineer Concurrency & Architecture Interview Set

---

## 🧵 Category 1: Thread Pools & Queue Boundaries

### Q1: The Danger of Unbounded Queues
* **Question:** When configuring a custom thread pool or task runner (like Celery or an internal app queue), you can set the queue capacity to be *bounded* (fixed size) or *unbounded* (infinite size). What is the operational risk of using an **unbounded queue** if your downstream database suddenly becomes incredibly slow or experiences a network partition?
* **What the interviewer is looking for:** Do you understand memory safety? They want you to mention that an unbounded queue will grow indefinitely during a traffic spike, eventually consuming all system RAM and triggering an Out-of-Memory (OOM) process crash.

### Q2: Deep Dive into "Caller-Runs" Backpressure
* **Question:** In a high-throughput system, when a bounded task queue fills up completely, the **Caller-Runs** policy forces the thread that *submitted* the task to execute it synchronously. 
  1. How does forcing the main thread to execute a task protect the system from crashing?
  2. What happens to the upstream client making the request while the main thread is busy executing that task?
* **What the interviewer is looking for:** Your mental model of execution flow. They want to hear that it introduces a natural "emergency brake" (backpressure) by halting new task submissions, though it temporarily increases latency for incoming requests.

---

## 🔒 Category 2: Race Conditions & Mutex Locks

### Q3: The Mechanics of a Critical Section
* **Question:** Look at this simple Python class snippet:
```python
  class Counter:
      def __init__(self):
          self.count = 0
      def increment(self):
          self.count += 1

```

If 100 threads execute `increment()` concurrently without a lock, the final value of `count` is almost always less than 100. Why does this happen? Explain what is happening at the step-by-step assembly/memory level.

* **What the interviewer is looking for:** Understanding that `self.count += 1` is not atomic. It consists of three distinct steps: **Read** the current value, **Modify** it in the CPU register, and **Write** it back to RAM. If threads overlap during these steps, updates get overwritten.

### Q4: Read-Write Locks vs. Standard Mutex Locks

* **Question:** If you are building a system where 95% of the operations are users reading data (e.g., viewing a movie theater seat map) and only 5% are writing data (booking a seat), why would using a standard `Mutex` lock on the entire read/write pipeline be inefficient? What primitive should you use instead?
* **What the interviewer is looking for:** Knowledge of optimization primitives. They want you to identify that a standard Mutex forces readers to wait in single-file lines unnecessarily. A **Read-Write Lock (RWLock)** allows infinite simultaneous readers but grants exclusive access to a single writer.

---

## 🚦 Category 3: Semaphores & Resource Throttling

### Q5: Counting Semaphore vs. Mutex Lock

* **Question:** Both Mutexes and Semaphores are used for synchronization, but they serve different core purposes. How does a **Counting Semaphore** initialized with a capacity of 3 handle thread access differently than a standard binary **Mutex Lock**?
* **What the interviewer is looking for:** Clear separation of concepts. A Mutex handles *exclusive ownership* (only 1 thread can hold it). A Semaphore handles *capacity management or signaling* (allowing up to $N$ threads to pass through simultaneously).

### Q6: Kernel-Level Thread Sleeping

* **Question:** When a thread pool runs out of database connections and a new worker thread calls `.acquire()` on an empty pool semaphore, what does the operating system kernel actually do to that thread? Why is this better than running a `while True: pass` loop?
* **What the interviewer is looking for:** Efficiency principles. They want to see that you understand **blocking**. A `while` loop spins the CPU at 100% utilization doing nothing (busy waiting). The kernel puts a blocked thread into a suspended sleep state, freeing up the CPU entirely for other processes.

---

## 🗺️ Category 4: Deadlocks & Prevention

### Q7: Identifying a Deadlock Blueprint

* **Question:** Can you explain the concept of a **Circular Wait** deadlock using a real-world scenario (like two bank accounts trying to transfer money to each other at the exact same moment)? What are the four mandatory conditions required for a deadlock to exist?
* **What the interviewer is looking for:** Familiarity with core theory (Coffman conditions) applied to practical code paths.

### Q8: The Magic of Resource Ordering

* **Question:** We can prevent deadlocks by sorting resource IDs (`if id_A < id_B`) before acquiring locks. Why does this simple sorting step completely eliminate the possibility of a deadlock?
* **What the interviewer is looking for:** Do you understand how changing the *locking order* forces competing threads into a predictable, non-overlapping linear queue, breaking the circular dependency ring entirely?

---

## 🌐 Category 5: Distributed System Fundamentals

### Q9: Monolithic Memory vs. Distributed Locking

* **Question:** If your Python code uses `threading.Lock()` to prevent two users from booking the same seat, that works perfectly on a single server. But what happens if your business grows and you deploy your application across **3 separate servers** behind a Load Balancer? Will `threading.Lock()` still prevent double bookings? How do you fix it?
* **What the interviewer is looking for:** Awareness of horizontal scaling. Threads on Server 1 cannot read Server 2's RAM. To solve this, you must extract the lock state to a centralized **Distributed Lock Manager (DLM)** like Redis.

### Q10: Optimistic Concurrency Control (OCC) / Versioning

* **Question:** Instead of locking a database row while a user is typing their checkout details (Pessimistic Locking), many junior engineers learn about **Optimistic Concurrency Control (OCC)** using version numbers. How does OCC work when updating a database record, and under what kind of traffic conditions does it perform poorly?
* **What the interviewer is looking for:** The trade-offs of locking strategies. They want you to explain that OCC checks if a version number changed before committing a write. If traffic contention is incredibly high (e.g., 1,000 people fighting for 1 seat), OCC causes massive retry storms, making explicit locking much better.
