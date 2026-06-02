# 🏗️ Design Principles Mastery Roadmap

| Principle | Practice Mini-Project Idea | The "Hands-on" Challenge | Status |
| :--- | :--- | :--- | :--- |
| **SRP** (Single Responsibility) | User Auth & Profile System | Separate user data, email validation, and database saving into three distinct classes. | ✅ **Done** |
| **OCP** (Open/Closed) | Shape Area Calculator | Add a `Circle` and `Triangle` to an existing system without modifying the `AreaCalculator` class. | ✅ **Done** |
| **LSP** (Liskov Substitution) | Bird Flight Simulator | Ensure that a `Penguin` (which can't fly) doesn't break a system expecting `FlyingBirds`. | ✅ **Done** |
| **ISP** (Interface Segregation) | Multi-Function Printer | Split a giant `IMachine` interface so a `SimpleScanner` isn't forced to implement `print()` or `fax()`. | ✅ **Done** |
| **DIP** (Dependency Inversion) | Message Notification Service | Make a `Notification` class depend on an `IMessageService` interface rather than a concrete `EmailService`. | ✅ **Done** |
| **DRY** (Don't Repeat Yourself) | App Configuration Utility | Abstract repetitive logic for reading environment variables into a single, authoritative helper. | ✅ **Done** |
| **KISS** (Keep It Simple) | Data Sorting Utility | Replace a complex, over-engineered pattern with a simple, readable Python built-in solution. | ✅ **Done** |
| **YAGNI** (You Ain't Gonna Need It) | Minimalist Feature Scoping | Refactor a project by removing "future-proof" code that hasn't been used in 3 months. | ✅ **Done** |
| **Composition over Inheritance** | RPG Character System | Build a `Warrior` using `CombatStyle` components instead of a deep, rigid class hierarchy. | ✅ **Done** |
| **Encapsulation** | Bank Account Balance | Refactor a code making variable private and using getter and setter | ✅ **Done** |
| **Law of Demeter** | Wallet & Customer Logic | Refactor `customer.get_wallet().get_cash().remove(amount)` to `customer.pay(amount)`. | ✅ **Done** |
| **Fail Fast** | Input Validation Guard | Implement "Guard Clauses" that raise exceptions immediately at the top of a function. | ✅ **Done** |
| **Separation of Concerns** | Three-Tier Web App | Separate UI presentation logic from the Business logic and Data Access logic. | ✅ **Done** |