# 🔬 GoF Design Patterns: Complete Architectural Board Exam

## 🏗️ PART 1: CREATIONAL PATTERNS

### Question 1: Abstract Factory vs. Factory Method
Your team is building a cross-platform video rendering app. 
* ***Scenario A:** You need a method that initializes a single video exporter (`MP4Exporter` or `WebMExporter`) depending on the user's settings.
* ***Scenario B:** You need to generate an entire matching ecosystem of UI components, background processors, and encoding codecs specifically configured for either *Windows High-Performance Mode* or *Mac Retina Mode*.
* **Task:** Identify which scenario requires the **Factory Method** and which requires the **Abstract Factory**, and explain the core difference between their intents.

### Question 2: The Builder Dilemma
You are designing a `NetworkRequest` class that has 2 mandatory fields (`url`, `method`) and 15 optional configurations (e.g., `timeout`, `headers`, `cookies`, `retry_count`, `cache_policy`). 
* **A.** What programming problem (often seen in constructors with many parameters) does the **Builder Pattern** eliminate here?
* **B.** How does the Builder pattern maintain **immutability** for the final `NetworkRequest` object during its step-by-step construction?

### Question 3: Singleton vs. Prototype
* **A.** In a multithreaded environment, what danger do you face when implementing a ***Singleton** Database Manager, and how do you protect against it?
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


## 🏎️ PART 3: BEHAVIORAL PATTERNS

### Question 7: Strategy vs. State
Both ***Strategy** and ***State** change the behavior of a context object dynamically at runtime by swapping out an internal reference to a behavior object.
* **A.** Who typically controls the swapping of the behavior object in the ***Strategy Pattern**?
* **B.** Who typically handles the transition from one behavior to another in the ***State Pattern**, and why?

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

<br>
<br>

# 🎓 GoF Design Patterns: Board Exam Grading & Architectural Feedback Report
You have just completed one of the most brutal software architecture tests possible: analyzing all 23 Gang of Four Design Patterns in a single sitting.

Your performance is outstanding. It is clear that doing the code challenges first gave you an exceptional intuitive grasp of how these patterns execute. Now that you've aligned them with design principles, you are thinking like an actual Software Architect.

Let's break down your answers, highlight your brilliant insights, and patch up a few critical misconceptions.

## 🏗️ PART 1: CREATIONAL PATTERNS
### Q1: Abstract Factory vs. Factory Method
**Score: 5 / 5 (Perfect)**

**Feedback:** Your distinction is flawless. You correctly recognized that Factory Method handles a single product variation (by letting subclasses decide which concrete exporter to instantiate), while Abstract Factory manages entire families of related products (the whole Windows vs. Mac ecosystem framework). Linking Factory Method to the Strategy pattern conceptually is a highly advanced, correct observation!

### Q2: The Builder Dilemma
**Score: 4.5 / 5 (Excellent)**

**Feedback:** 
* Part A: Spot on. You perfectly described avoiding the "Telescoping Constructor" problem where you have to pass long trails of None values and accurately track the exact argument index position.

* Part B: Your explanation of the mechanics is accurate. To get the remaining 0.5 points for total architect level completeness: the secret to maintaining immutability is that the Builder itself is mutable while you append values, but the target NetworkRequest object is only instantiated at the very last second inside the .build() method. The NetworkRequest class itself does not have any setter methods, making it completely immutable once born.

### Q3: Singleton vs. Prototype
**Score: 5 / 5 (Perfect)**

**Feedback:** 
* Part A: You correctly called out the classic multithreading race condition trap where multiple threads could simultaneously slide past a if instance is None: check and create separate instances. Your solution—Thread Locking—is exactly how to secure it.

* Part B: Excellent description of a heavy-loading bottleneck. You beautifully explained the structural difference between a shallow copy (copying pointers/top layer) and a deep copy (cloning the entire recursive data tree). Skipping the costly 5–10 second I/O initialization asset load via cloning an in-memory Prototype is a textbook use case.

## 🧱 PART 2: STRUCTURAL PATTERNS
### Q4: Decorator vs. Proxy
**Score: 2.5 / 5 (Critical Misconception in Part B)**

**Feedback:** 
* Part A: Your explanation of intent is perfectly correct. Decorator expands/augments an object's behavior dynamically, while Proxy controls, restricts, or delays access to the underlying object.

* Part B (The Error): You chose Decorator to intercept a database call for Admin permissions. This should actually be a Proxy (specifically, a Protection Proxy). * Why? A Decorator is used when you want to stack features on top of each other (like adding Bold and Underline to text). If a non-admin user logs in, you don't want to decorate their database query with extra behavior; you want to block them at the gate. A Protection Proxy intercepts the call, evaluates the credentials, and decides whether to forward the call to the real database object or raise an Access Denied exception.

### Q5: Composite Architecture
**Score: 5 / 5 (Perfect)**

**Feedback:** Splendid explanation! You identified the three key pillars: Component, Leaf, and Composite. By making both Employee and Department implement the exact same get_budget() interface method, you completely stripped out the need for messy, anti-pattern isinstance() checks. The top-level application treats single leaves and complex branches identically.

### Q6: Adapter vs. Facade vs. Bridge
**Score: 5 / 5 (Perfect)**

**Feedback:** 
* Adapter: Correct. Converting incompatible data structures (XML ➡️ JSON) is the ultimate definition of an Adapter.

* Facade: Correct. You described providing a clean, single-point-of-entry helper method (start_stream()) to hide a chaotic mess of underlying subsystems.

* Bridge: Phenomenal answer. You correctly noted that by decoupling the remote abstractions from the underlying brand implementations, you avoid a combinatorial class-explosion matrix and let both sides grow independently.

## 🏎️ PART 3: BEHAVIORAL PATTERNS
### Q7: Strategy vs. State
**Score: 5 / 5 (Perfect)**

**Feedback:** This is one of the toughest questions on the exam, and you nailed it. In Strategy, the client or main context explicitly changes or passes the tool configuration. In State, the states themselves contain the internal transition transitions, flowing automatically from one condition to another based on actions, completely encapsulating state management away from the client.

### Q8: The Command Pattern & Undo Mechanics
**Score: 3 / 5 (Partial Answer)**

**Feedback:** While you correctly called out that the Memento pattern can be used in tandem to snapshot states, the question asked what each concrete Command object must structurally implement on its interface to support a history stack.

To make an Undo stack work using pure Command architecture, every Command interface must implement two explicit methods: execute() (to perform the operation) and undo() (to reverse it). Additionally, the command object must store its own contextual state (like the deleted text characters) during execute() so it knows exactly what to restore when undo() is popped off the history list.

### Q9: Observer vs. Chain of Responsibility
**Score: 5 / 5 (Perfect)**

**Feedback:** Outstanding structural analysis. You perfectly contrasted the communication styles: Observer is a broad One-to-Many broadcast (everyone on the subscriber registry list gets notified simultaneously), whereas Chain of Responsibility is a linear One-to-One pass-along chain that can short-circuit and stop early the moment an authorized handler resolves the request.

### Q10: Template Method vs. Iterator vs. Memento
**Score: 5 / 5 (Perfect)**

**Feedback:** 
* Template Method: Great parsing algorithm example! You elegantly showed how locking the macro-steps (get -> upload -> parse -> store) keeps the core algorithm closed for modification, while leaving individual steps abstract keeps it open for extension.

* Iterator: Brilliant explanation. Exposing structural node traversal (.left, .right) leaks internal tree layouts. Wrapping it inside a unified .next() call maintains clean encapsulation.

* Memento: Perfect. The Caretaker is just a blind history manager. It holds the memento boxes but isn't allowed to see inside them, preserving the original object's data encapsulation.

### Q11: Visitor vs. Interpreter
**Score: 5 / 5 (Perfect)**

**Feedback:** 
* Interpreter: Correct. Evaluating a custom expression syntax tree into a calculated layout is exactly what Interpreter is designed for.

* Visitor: Your geometric example is beautiful. By creating a separate ExportSVGVisitor and passing elements via an .accept(visitor) double-dispatch mechanism, you successfully added new operations across all shapes without altering their native source files.

## 📊 Final Board Exam Score: 50.5 / 55 (92% - Honors Architect)
Aside from the minor structural details on the Command layout and the classic conceptual mix-up between a Decorator and an Access-Control Proxy, your architectural intuition is incredible. You don't just memorize definitions; you truly understand how components communicate, decouple, and scale.

You have officially conquered both Design Principles and Design Patterns!