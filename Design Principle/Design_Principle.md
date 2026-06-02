# 🏗️ Software Design Principles

Design Principles are high-level guidelines that help developers create software that is easy to maintain, extend, and understand. Unlike Design Patterns (which are specific solutions to common problems), Principles are general "rules of thumb" to keep code clean.

---

## 💎 Core Design Principles

These are the fundamental concepts that every developer should follow to avoid "Rotting Code."

### 1. SOLID Principles
The most famous set of principles for Object-Oriented Design.
*   **S - Single Responsibility (SRP):** A class should have only one reason to change.
*   **O - Open/Closed (OCP):** Software entities should be open for extension but closed for modification.
*   **L - Liskov Substitution (LSP):** Subtypes must be substitutable for their base types without breaking the app.
*   **I - Interface Segregation (ISP):** Clients should not be forced to depend on methods they do not use.
*   **D - Dependency Inversion (DIP):** Depend on abstractions, not concretions.

### 2. DRY (Don't Repeat Yourself)
Every piece of knowledge must have a single, unambiguous, authoritative representation within a system. If you see the same logic in two places, abstract it.

### 3. KISS (Keep It Simple, Stupid)
Systems work best if they are kept simple rather than made complicated. Avoid over-engineering and unnecessary patterns for simple tasks.

### 4. YAGNI (You Ain't Gonna Need It)
Do not add functionality until it is necessary. Don't build a complex "plugin system" if you only have one plugin today.

### 5. Composition Over Inheritance
It is usually better to achieve polymorphic behavior and code reuse by composing objects (having a reference to another class) rather than inheriting from a base class.

### 6. Encapsulation
Hide the internal state and requiring all interaction to be performed through a well-defined interface. Protect your data!

### 7. Separation of Concerns (SoC)
The program should be split into distinct sections, where each section addresses a separate concern (e.g., UI logic vs. Database logic).

---

## 📂 Design Principle Categories

| Category | Description | Key Topics |
| :--- | :--- | :--- |
| **Maintainability** | Making code easy to fix and update. | DRY, SoC, SRP |
| **Flexibility** | Making code easy to change or extend. | OCP, DIP, LSP |
| **Simplicity** | Reducing cognitive load for developers. | KISS, YAGNI |
| **Coupling/Cohesion** | Managing how classes depend on each other. | Low Coupling, High Cohesion |

---

## 📋 Detailed Topic Overview

### 🧱 Low Coupling & High Cohesion
*   **Low Coupling:** Classes should be as independent as possible. Changing one shouldn't break ten others.
*   **High Cohesion:** Everything inside a single class should be closely related to its purpose.

### 🔌 Inversion of Control (IoC)
Instead of a class creating its own dependencies, they are "injected" from the outside (Dependency Injection).

### 🛡️ Law of Demeter (Least Knowledge)
A module should not know about the inner workings of the objects it manipulates. "Only talk to your immediate friends."

### ⚖️ Fail Fast
Report errors as soon as they occur rather than trying to proceed with "garbage" data, which makes debugging much harder.

### 🚀 Boy Scout Rule
"Always leave the code cleaner than you found it." Small, constant improvements prevent technical debt.

---

## 🎯 The Goal of Design Principles
The ultimate goal is to reduce **Technical Debt**. Code that follows these principles is:
1.  **Readable:** New developers can understand it quickly.
2.  **Testable:** Logic is isolated, making unit testing easy.
3.  **Scalable:** You can add new features without a "domino effect" of bugs.

---

### **Encapsulation**
*   Bundle data and methods together and restrict access to the inner workings (using `private`/`protected`).
*   Protect the "Internal State."

### **Separation of Concerns (SoC)**
*   Divide a program into distinct sections, each addressing a separate concern (e.g., Logic vs. UI vs. Storage).

### **Law of Demeter (Least Knowledge)**
*   "Only talk to your immediate friends." 
*   A method should only call methods of its own class, its parameters, or objects it created. Don't do: `obj.getA().getB().doSomething()`.

### **Inversion of Control (IoC)**
*   Instead of your code calling a library, the framework calls your code. 
*   This is the "Hollywood Principle": *Don't call us, we'll call you.*

---

## 📊 4. Metrics for Success

| Metric | Description | Desired State |
| :--- | :--- | :--- |
| **Coupling** | How much classes depend on each other. | **Low** (Independent) |
| **Cohesion** | How focused a class is on a single task. | **High** (Focused) |
| **Technical Debt**| The cost of choosing an easy solution now vs. a better one later. | **Low** |
| **Fail-Fast** | Reporting errors immediately when they occur. | **High** |

---

## 🎯 The "Boy Scout Rule"
> *"Always leave the code cleaner than you found it."*
Small, incremental improvements every day prevent the code from rotting over time.