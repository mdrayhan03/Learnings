# 📝 System Design Execution & Concurrency Mastery Exam

**Instructions:** Answer the following questions using clear architectural reasoning, low-level design patterns, pseudo-code, or mathematical justifications where appropriate.

---

## 🏛️ Section 1: State Engines & Lifecycle Systems

### Q1: Distributed Vending Machine State Matrix
You designed a state machine engine using a 2D State Transition Matrix ($O(1)$ lookups) rather than the standard State Pattern class-swapping.
* **Scenario:** The machine is currently in the `Dispensing` state. An unexpected hardware sensor failure occurs mid-dispense, requiring a transition to `Maintenance`. 
* **Questions:**
  1. How do you design your transition table/matrix structurally to handle *invalid* state transitions safely without throwing generic nested `if/else` errors?
  2. If two threads concurrently trigger inputs (e.g., `CoinInserted` and `MaintenanceOverride`) at the exact same millisecond, how do you prevent the state transition matrix from executing a race condition transition?

### Q2: Multi-Cabin Elevator Fleet Controller Lifecycle
You used a combination of Min/Max Heaps to schedule floors for a 4-cabin elevator fleet.
* **Scenario:** Elevator 1 is in state `Moving_Up` at Floor 4, aiming for Floor 10. A user on Floor 6 presses the "Up" button, while a user on Floor 5 presses the "Down" button.
* **Questions:**
  1. Explain how your Min/Max Heap layout decides which requests get assigned to Elevator 1 versus a secondary `Idle` elevator.
  2. How do you prevent a high-floor demand spike from causing **starvation** for low-floor requests in this specific heap configuration?

---

## 📊 Section 2: Resource Management & Spatial Allocation

### Q3: Multi-Floor Parking Lot Allocation Engine
Your allocation engine uses categorized Min-Heaps to search and assign parking slots across 5 floors in $O(\log N)$ time.
* **Scenario:** A slot becomes free on Floor 2. At the exact same moment, 3 separate driver threads are querying the Min-Heap for an available spot.
* **Questions:**
  1. In a multi-threaded language, how do you protect the internal array structure of the Min-Heap during concurrent `.pop()` and `.push()` heapify operations?
  2. If you must support a new feature—*Reserving a specific spot for a VIP customer*—how does that alter your $O(\log N)$ heap-based allocation strategy?

### Q4: Flight/Hotel Matrix Capacity Map
You modeled a compact, real-time booking grid tracking contiguous seating blocks.
* **Scenario:** A family requests a block of 4 contiguous seats together in a single row. 
* **Questions:**
  1. What underlying bitwise or matrix data structure did you choose to ensure finding contiguous blocks is optimized without scanning the entire 2D array sequentially ($O(R \times C)$)?
  2. When a user is in the checkout phase (holding 4 seats for 5 minutes), how do you model the seat state (`Available`, `Reserved`, `Locked`) to prevent other queries from reading outdated availability mapping data?

---

## ⚡ Section 3: Code-Level Concurrency & Synchronization Primitives

### Q5: Thread-Safe Movie Ticket Engine
You simulated 1,000 threads contending for the exact same concert seat at the exact same millisecond.
* **Scenario:** Thread A reads that Seat 42 is unbooked. Before Thread A can mark it booked, Thread B also reads that Seat 42 is unbooked.
* **Questions:**
  1. Sketch the exact code sequence or lifecycle diagram showing how a **Mutex Lock** or an **Atomic Compare-And-Swap (CAS)** instruction enforces that only one thread succeeds.
  2. Why would using a standard Read-Write Lock (`RWLock`) be an anti-pattern for this specific ticket reservation checkout step?

### Q6: Throttling via Payment Connection Pools
You built a Connection Pool throttling database sockets using a Counting Semaphore and a secondary Mutex Lock.
* **Scenario:** Your pool has a capacity of $N=3$. Five threads call `.get_connection()` at the same time.
* **Questions:**
  1. Why can't a `Semaphore` handle the internal array mutation (`_pool.pop(0)`) by itself? What specific bug occurs if you remove the secondary Mutex Lock?
  2. Explain step-by-step what happens inside the operating system kernel when Thread 4 calls `.acquire()` on an exhausted semaphore.

### Q7: Deadlock Prevention in Bank Transfer Engines
You designed a multi-account fund transfer engine processing cyclic concurrent operations ($A \rightarrow B$ and $B \rightarrow A$).
* **Scenario:** You are using **Resource Ordering** to sort account IDs before acquiring locks.
* **Questions:**
  1. Prove mathematically or logically how sorting account identifiers ($ID_{low}$ then $ID_{high}$) explicitly breaks the **Circular Wait** condition.
  2. If you migrate this monolith to a microservice distributed cluster across 5 separate servers using a shared Redis instance, how does your locking strategy change to handle network delays or node crashes?

### Q8: Custom Bounded Thread Pools & Backpressure
You constructed a custom thread pool utilizing a bounded FIFO queue and the **Caller-Runs** rejection policy.
* **Scenario:** The background worker pool is fully occupied processing slow log requests, and the bounded queue is completely full ($Capacity = 10$). A new log event arrives.
* **Questions:**
  1. Walk through the runtime mechanics of the **Caller-Runs Policy**. How does forcing the main ingestion thread to process the log directly protect the application from crashing due to an Out-of-Memory (OOM) exception?
  2. What is a "Poison Pill" task payload, and how do your long-lived worker threads utilize it to achieve a zero-data-loss graceful shutdown?

---

## 🧬 Section 4: Advanced Cross-Cutting Scenarios

### Q9: The Read/Write Ledger Hotspot Problem
* **Scenario:** Imagine an account or a specific seat that experiences an extreme volume of read requests (thousands of users viewing the seat map status) but a low volume of write requests (only one actual booking change). 
* **Question:** How do you optimize your synchronization strategy to maximize concurrent read throughput without creating a bottleneck on the eventual write mutation?

### Q10: Memory Leakage in Long-Lived Task Queues
* **Scenario:** In your high-throughput log processor thread pool, some log tasks hold onto massive data chunks (e.g., large string payloads or diagnostic context references).
* **Question:** If a worker thread finishes executing a task but remains alive inside the infinite loop, what architectural patterns or cleanup steps must be performed on the task queue payloads to ensure memory is released immediately by the garbage collector or memory allocator?