# 🔬 GoF Design Patterns: Complete Architectural Board Exam

## 🏗️ PART 1: CREATIONAL PATTERNS

### Question 1: Abstract Factory vs. Factory Method
Your team is building a cross-platform video rendering app. 
* **Scenario A:** You need a method that initializes a single video exporter (`MP4Exporter` or `WebMExporter`) depending on the user's settings.
* **Scenario B:** You need to generate an entire matching ecosystem of UI components, background processors, and encoding codecs specifically configured for either *Windows High-Performance Mode* or *Mac Retina Mode*.
* **Task:** Identify which scenario requires the **Factory Method** and which requires the **Abstract Factory**, and explain the core difference between their intents.

### Question 2: The Builder Dilemma
You are designing a `NetworkRequest` class that has 2 mandatory fields (`url`, `method`) and 15 optional configurations (e.g., `timeout`, `headers`, `cookies`, `retry_count`, `cache_policy`). 
* **A.** What programming problem (often seen in constructors with many parameters) does the **Builder Pattern** eliminate here?
* **B.** How does the Builder pattern maintain **immutability** for the final `NetworkRequest` object during its step-by-step construction?

### Question 3: Singleton vs. Prototype
* **A.** In a multithreaded environment, what danger do you face when implementing a **Singleton** Database Manager, and how do you protect against it?
* **B.** In a game engine, why is cloning an existing instance using the **Prototype Pattern** faster and more memory-efficient than repeatedly calling standard object instantiation (`__init__` or `new`) for 100 separate monster units?

---

## 🧱 PART 2: STRUCTURAL PATTERNS

### Question 4: Decorator vs. Proxy
Both the **Decorator** and **Proxy** patterns use composition to wrap a target object and share the exact same interface as the object they are wrapping.
* **A.** If their structures look nearly identical in code, what is the fundamental difference in their **intent**?
* **B.** If you want to add a feature that intercepts a database call to check if the current user has "Admin" permissions before executing the query, which pattern should you use?

### Question 5: Composite Architecture
You are building an organizational chart application. The system needs to calculate the total salary budget for various departments. A `Department` can contain individual `Employee` objects, but it can also contain *sub-departments*, which themselves contain more employees.
* **Task:** Explain how the **Composite Pattern** allows a client script to calculate the total budget of a top-level department seamlessly without using `isinstance()` checks or complex nested loops.

### Question 6: Adapter vs. Facade vs. Bridge
* **A.** You have a 3rd-party analytics library that outputs data in XML format, but your main dashboard only accepts JSON. Which pattern closes this gap?
* **B.** You have a massive, chaotic subsystem consisting of 15 micro-classes (audio mixers, video buffers, thread lockers). You want to give the client a simple `start_stream()` button. Which pattern do you use?
* **C.** You are designing a system where you have multiple types of `RemoteControl` abstractions and multiple types of `TV/Radio` implementations. You want to grow the remotes and the devices independently without creating a matrix of `SonyRemoteForRadio`, `SamsungRemoteForTV`, etc. How does the **Bridge Pattern** structurally solve this?

---

## 🏎️ PART 3: BEHAVIORAL PATTERNS

### Question 7: Strategy vs. State
Both **Strategy** and **State** change the behavior of a context object dynamically at runtime by swapping out an internal reference to a behavior object.
* **A.** Who typically controls the swapping of the behavior object in the **Strategy Pattern**?
* **B.** Who typically handles the transition from one behavior to another in the **State Pattern**, and why?

### Question 8: The Command Pattern & Undo Mechanics
You are building a text editor like Microsoft Word. You implement the **Command Pattern** to execute text operations like `InsertTextCommand` and `DeleteTextCommand`.
* **Task:** To support an **Undo/Redo stack**, what two essential pieces of information or structural methods must each concrete `Command` object implement?

### Question 9: Observer vs. Chain of Responsibility
* **A.** When a `Publisher` triggers an update in the **Observer Pattern**, which observers receive the broadcast?
* **B.** When a `SupportTicket` enters a **Chain of Responsibility**, how many handlers along the chain typically execute and resolve the request? What is the structural difference in how messages flow between these two patterns?

### Question 10: Template Method vs. Iterator vs. Memento
* **A.** How does **Template Method** enforce the Open/Closed Principle (OCP) when defining a broad data-parsing algorithm?
* **B.** How does the **Iterator Pattern** respect Encapsulation when navigating a complex tree data structure?
* **C.** Why does a **Memento** object intentionally hide its internal state snapshot from the outside `Caretaker` class that manages the save history?

### Question 11: Visitor vs. Interpreter
* **A.** You have a complex syntax tree representing a custom formula layout (e.g., `"5 PLUS 3"`). Which pattern evaluates this syntax tree into a numerical result?
* **B.** You have a fixed system of geometric elements (`Circle`, `Square`). You want to add a brand-new operational feature (e.g., `export_to_svg()`, `calculate_perimeter()`) without changing any code inside the `Circle` or `Square` classes. How does the **Visitor Pattern** make this possible?