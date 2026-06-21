# 🔬 Production-Grade Low-Level Design (LLD) Mastery Exam

This exam evaluates your ability to translate abstract requirements into clean, maintainable, extensible, and thread-safe Object-Oriented code. 

### 🔏 Rules of Execution:
1. **SOLID Compliance:** Every design must strictly adhere to SOLID principles.
2. **No Type-Checking Violations:** Avoid `isinstance()`, `type()`, or massive structural `switch/case` walls that inspect object types. Use polymorphism instead.
3. **Thread Safety:** Medium and Hard problems *must* explicitly account for concurrent execution threads accessing shared resources simultaneously.
4. **Encapsulation:** Keep internal states protected. Use explicit guard clauses to fail fast.

---

## 🟢 STEP 1: EASY (Single Component Mechanics & Structural Cleanliness)
*Focus: Mastering basic encapsulation, preventing data leaks, and applying structural GoF patterns cleanly.*

### Question 1: The Unified Notification Dispatcher(done)
* **Scenario:** You are building an enterprise alert system. The system must support sending notifications via `Email`, `SMS`, and `Slack Push`. 
* **Requirements:**
  * The core application business logic should not care which delivery mechanism is being used.
  * You need to be able to add a new delivery mechanism (e.g., `WhatsApp`) in the future without changing a single line of code in the core business module or the existing dispatchers.
  * Users can configure their profiles to send an alert via *both* Email and Slack simultaneously using a single invocation.
* **Task:** Write the class structure and interfaces using the **Strategy** and **Decorator/Composite** patterns to achieve this setup cleanly.

### Question 2: The Multi-Format Custom Configuration Parser(done)
* **Scenario:** Your application needs to read configuration settings. The configurations can come from a standard `.json` string, an `.xml` payload, or an environment variable mapping.
* **Requirements:**
  * The internal application client only speaks native Python dictionaries.
  * It should be impossible for the client to instantiate the wrong parsing subsystem directly; instantiation logic must be fully centralized.
* **Task:** Implement the structural layout using the **Factory Method** or **Adapter** pattern to translate these incompatible formats into a single, unified interface.

---

## 🟡 STEP 2: MEDIUM (Multi-Entity Real-World Simulations & State Engines)
*Focus: Tracking entity relationships, matrix layouts, allocations, and managing complex lifecycles using state tracking.*

### Question 3: The Automated Vending Machine Engine(done)
* **Scenario:** Design the core logic for a physical vending machine. 
* **Requirements:**
  * **The States:** `IdleState` (No money inserted), `HasMoneyState` (Money inserted, waiting for selection), `DispensingState` (Processing inventory release), and `OutOfStockState`.
  * **The Actions:** `insert_money(amount)`, `select_product(product_id)`, `dispense()`, and `cancel_transaction()`.
  * **The Rules:** If a user calls `insert_money()` while the machine is in `DispensingState`, it must raise an exception or reject it. If they click `cancel_transaction()` while in `HasMoneyState`, the machine must return their change and transition back to `IdleState`.
* **Task:** Implement this entire behavioral infrastructure utilizing the **State Pattern** without using a single nested `if/else` block to check the machine's state variable. **Ensure thread safety during product allocation.**

### Question 4: The Multi-Level Parking Lot System
* **Scenario:** Design a backend for a commercial `ParkingLot`.
* **Requirements:**
  * The parking lot contains multiple `Floor` objects. Each floor contains a specific allocation of `ParkingSpot` layouts: `Compact` (for Motorcycles), `Medium` (for Cars), and `Large` (for Trucks).
  * A `Vehicle` object has a specific type (`Motorcycle`, `Car`, `Truck`).
  * **The Challenge:** A `Truck` can only fit into a `Large` spot. A `Car` can fit into a `Medium` or `Large` spot. A `Motorcycle` can fit into any spot.
  * You must implement a `park_vehicle(vehicle)` method that automatically assigns the closest available valid spot to the vehicle, marks it occupied, and generates a `ParkingTicket`.
* **Task:** Sketch the object-oriented structure. Apply the **Open/Closed Principle** so that if an `ElectricVehicle` requiring an `ElectricChargingSpot` is added later, the allocation engine requires zero internal modifications.

---

## 🔴 STEP 3: HARD (High-Concurrency Production Engines)
*Focus: Thread synchronization, race condition elimination, transaction atomic safety, and memory-efficient object lifecycles.*

### Question 5: Thread-Safe Movie Ticket Booking Engine
* **Scenario:** You are building the core reservation model for a high-traffic cinema platform.
* **Requirements:**
  * A `Show` has a finite grid of `Seat` objects (e.g., `Row G, Seat 12`). Each seat has a state: `Available`, `Locked` (temporarily held in a user's checkout cart for 5 minutes), or `Booked`.
  * **The Concurrency Nightmare:** 10,000 users are simultaneously vying for the exact same popular seat (`G12`) at the exact same millisecond. 
  * Your backend must ensure that **exactly one** thread successfully executes the lock/booking sequence, while the other 9,999 colliding threads are rejected cleanly with a thread-safe exception (`SeatUnavailableException`) without crashing, entering deadlocks, or leaking memory.
* **Task:** Write out the complete Python/pseudo-code implementation of the `BookingEngine` and `Seat` components showing how you handle thread synchronization (`Threading.Lock`, mutexes, or atomic check-and-set guards) to maintain absolute transactional integrity.

### Question 6: High-Frequency Stock Brokerage Order Matching Engine
* **Scenario:** Design an internal matching engine for a financial trading platform.
* **Requirements:**
  * The system processes `Order` objects. An order can be a `BuyOrder` or a `SellOrder` for a specific stock ticker (e.g., `GOOG`), containing a `quantity` and a target `price`.
  * The engine holds an `OrderBook`. When a new `BuyOrder` enters, the engine must look through available `SellOrders`. If a matching price is found, it must execute a trade transaction and update both orders' remaining quantities.
  * Millions of orders are poured into the matching engine asynchronously across hundreds of concurrent background worker threads.
* **Task:** Structure the application objects. What internal data structures (e.g., Priority Queues, Red-Black Trees, thread-safe HashMaps) will you use inside your classes to ensure that orders are matched efficiently ($O(1)$ or $O(\log N)$) while maintaining complete thread-safe accuracy across the entire matching pipeline?