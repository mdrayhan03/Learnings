# SOLID
### S - Single Responsibility Principle (SRP)
The Rule: A class should have one, and only one, reason to change.

If a class does three different things (e.g., handles data, processes logic, and prints to the console), it is "coupled." Changing the way you print will force you to touch the data logic, risking bugs.

### O - Open/Closed Principle (OCP)
The Rule: Software entities (classes, modules, functions) should be open for extension, but closed for modification.

This means you should be able to add new functionality without changing existing code. If you have to open a class and add if/else statements every time a new requirement comes in, you are breaking OCP.

### L - Liskov Substitution Principle (LSP)
The Rule: Subtypes must be substitutable for their base types without breaking the application.

In simple terms: A subclass should behave exactly like its parent class expect for its specific internal logic. It should not alter expected behaviors, narrow down parameters, throw unexpected errors, or return completely different data types. If a subclass has an overridden method that does nothing, returns None unexpectedly, or raises a NotImplementedError, you have violated LSP.

### I - Interface Segregation Principle (ISP)
The Rule: Clients should not be forced to depend on methods they do not use.

In languages like Python (which uses duck typing), this principle translates to: Keep your interfaces/abstract classes lean. Don't create a massive "fat interface" that forces subclasses to implement dummy methods just to satisfy the abstract class contract.

### D - Dependency Inversion Principle (DIP)
The Rule: High-level modules should not depend on low-level modules. Both should depend on abstractions.

In simple terms: Your business logic should not directly import and depend on hardcoded tools (like a specific database, a specific email sender, or a specific API client). Instead, your business logic should depend on a generic interface, and the concrete tool should be plugged in from the outside.

| Principle | Practice Mini-Project Idea | The "Hands-on" Challenge | Status |
| :--- | :--- | :--- | :--- |
| **SRP** (Single Responsibility) | User Auth & Profile System | Separate user data, email validation, and database saving into three distinct classes. | ✅ **Done** |
| **OCP** (Open/Closed) | Shape Area Calculator | Add a `Circle` and `Triangle` to an existing system without modifying the `AreaCalculator` class. | ✅ **Done** |
| **LSP** (Liskov Substitution) | Bird Flight Simulator | Ensure that a `Penguin` or `Ostrich` doesn't break a system expecting `FlyingBirds`. | ✅ **Done** |
| **ISP** (Interface Segregation) | Multi-Function Printer | Split a giant `IMachine` interface so a `SimpleScanner` isn't forced to implement `print()` or `fax()`. | ✅ **Done** |
| **DIP** (Dependency Inversion) | Message Notification Service | Make a `Notification` class depend on an `IMessageService` interface rather than a concrete `EmailService`. | ✅ **Done** |

# DRY
Don't Repeat Yourself sounds like the simplest rule in coding, but it runs much deeper than just copy-pasting code.

The true definition of DRY is: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

It's not just about matching lines of text; it's about matching business logic. If you have the exact same rule written in two different places, and that rule changes tomorrow, you have to remember to change it in both places. If you forget one, your system breaks.

# KISS
Keep It Simple, Stupid <br>
The Rule: Systems work best if they are kept simple rather than made complicated. Avoid over-engineering, unnecessary abstractions, and heavy patterns for simple problems.

As developers grow in experience, they often fall into the trap of "Patternitis"—applying complex patterns everywhere just because they can, which makes the code incredibly hard to read and navigate.

# YAGNI
You Ain't Gonna Need It
The Rule: Do not add functionality or code complexity until it is explicitly necessary.

YAGNI is the sibling of KISS. It stops you from writing code for hypothetical future features. Developers often think, "We don't need this feature today, but what if the client asks for it in 6 months? Let me build the foundation for it now." 90% of the time, that future requirement never happens, or it changes completely, meaning you wasted time writing and maintaining dead code.

# Composition Over Inheritance
The Rule: It is usually better to achieve polymorphic behavior and code reuse by composing objects (giving a class a reference to another class) rather than inheriting from a base class.

Inheritance creates a rigid relationship ("Is-A"). If a child class inherits from a parent, it inherits everything, even if it doesn't need it. Composition creates a flexible relationship ("Has-A"), allowing you to swap behaviors at runtime.

# Encapsulation
The Rule: Hide the internal state of an object and require all interaction to be performed through a well-defined public interface. Protect your variables from outside tampering!

In Python, there are no strict private keywords like in Java or C++. Instead, we use conventions:

_variable: Tells other developers "Please treat this as private."

__variable: Triggers Name Mangling, making it harder (but not impossible) to access directly from the outside.

@property: Creates clean getters and setters.

# Law of Demeter
The Rule: A module should not know about the inner workings of the objects it manipulates. It should only talk to its immediate friends, not its friends' friends.

When you see "chained" method calls like a.get_b().get_c().do_something(), you are violating the Law of Demeter. This creates High Coupling. If the structure of C changes, your code breaks, even though your class only directly deals with A.

# Separation of Concerns (SoC)
The Rule: A software system should be split into distinct sections, where each section addresses a separate "concern" or feature of the program.

SoC is the grand architectural umbrella that sits above principles like SRP. While SRP says "a single class should only have one job," SoC looks at the macro level and says "different layers of your application should not mix." The most common real-world violation of SoC is mixing Business Logic (calculations and database queries) with Presentation Logic (printing things, building HTML tables, or accepting console inputs).

# Fail Fast (The Input Validation Guard)
The Rule: Report errors as soon as they occur rather than trying to proceed with "garbage" or invalid data.

Instead of nesting your core business logic inside deep, multiple layers of if-else blocks (which creates what developers call the "Pyramid of Doom"), use Guard Clauses at the very top of your function to catch issues early and exit immediately.

# 🧩 Low Coupling vs. High Cohesion
| Concept | The Rule,Real-World Meaning | Your Inventory Code Example |
| :--- | :--- | :--- |
| Low Coupling | Classes should be as independent as possible. Changing one should not break others.,A change to how a view prints text shouldn't crash the calculation logic. | InventoryConsoleView only expects a simple dictionary. It doesn't care how the database fetches it. |
| High Cohesion | Everything inside a single class should be closely related to its core purpose.,"Don't create ""kitchen sink"" classes. Keep focus tight." | InventoryService only deals with data and calculations. It does not contain string wrappers or terminal layouts. |