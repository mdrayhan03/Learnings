# 🎓 System & Presentation Architecture Mastery Exam

## Section 1: Theoretical Depth (Short Answer / Conceptual)

### Question 1: The Outward Dependency Rule
In Clean or Onion Architecture, why are databases, ORMs (like Django ORM or SQLAlchemy), and third-party API clients placed on the absolute **outermost** layer? What catastrophic problem occurs if an entity class in the core domain imports a database model class directly?

### Question 2: Sync vs. Async Distributed Boundaries
Compare your **Microservices** implementation with your **Event-Driven Architecture (EDA)** implementation:
* Explain what happens to the availability of the `BookingService` if the `UserService` goes down completely in your Microservices layout.
* Contrast this with what happens to the `OrderService` if the `EmailNotificationService` crashes in your EDA setup. 

### Question 3: The Presentation Pivot Point
Both **MVP** and **MVI** were created to solve problems found in patterns that came before them. 
* Exactly what problem does MVP solve regarding the relationship between the **View** and the **Model** in classic MVC?
* Exactly what problem does MVI solve regarding the synchronization mechanics found in highly complex **MVVM** data-binding setups?

---

## Section 2: Descriptive Architecture & Trade-offs (Scenario-Based)

### Scenario A: High-Scale Analytics Engine
You are the Lead Architect at a ride-sharing tech company. The marketing team wants to add a real-time behavioral analytics tracking dashboard that tracks where users click, search, and abandon rides. This module will process 50,000 telemetry events per second. 

* **The Dilemma:** An entry-level engineer suggests adding an execution route inside your existing, single-instance **Layered (N-Tier)** backend monolith that writes these telemetry tracking items straight to your primary relational PostgreSQL database.
* **Your Task:** Provide a descriptive architectural critique of this approach. Which pattern from your master tracker (**CQRS**, **Microservices**, or **EDA**) should be introduced here to save the platform from crashing under load, and how would you structure the topology?

### Scenario B: The Swappable Frontend Interface
Your team needs to build a critical inventory-tracking system that will be used by factory workers on rugged android tablets, by corporate admins via a React web dashboard, and by terminal server technicians via an SSH command-line interface. The data-saving logic and business validation rules for calculating inventory are completely identical for all three groups.

* **Your Task:** Choose **one** presentation pattern from your ledger (**MVC**, **MVP**, **MVVM**, or **MVI**) that would make it easiest to develop these three completely distinct user interfaces while keeping 100% of your business calculations, form evaluations, and data routing rules in a single, shared, reusable code asset. Describe exactly how the boundaries would be drawn.

---

## Section 3: Code-Based Structural Audits (Refactoring Challenges)

### Challenge 1: The Hexagonal Boundary Breach
The following Python script claims to follow **Hexagonal (Ports & Adapters)** architecture, but it contains an architectural violation that tightly couples the application core to an external infrastructure choice. 

**Identify the architectural violation line, explain why it breaks Hexagonal isolation rules, and rewrite the code correctly.**

```python
from abc import ABC, abstractmethod
import pymongo # External Database Client Library

# Infrastructure/Port Boundary
class INotificationPort(ABC):
    @abstractmethod
    def send(self, user_id: int, message: str) -> None: pass

# Core Business Application Logic
class RegistrationUseCase:
    def __init__(self, notifier: INotificationPort):
        self.notifier = notifier

    def register_user(self, user_id: int, username: str) -> None:
        print(f"[Core] Registering user: {username}")
        # Imagine registration logic happens here...
        
        # Business Rule: Alert the user
        self.notifier.send(user_id, "Welcome to our platform!")

# Infrastructure/Adapter Layer
class MongoAlertAdapter(INotificationPort):
    # AUDIT THIS CODE BLOCK:
    def send(self, user_id: int, message: str) -> None:
        # Connect directly to a specific hardcoded database instance client
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["system_logs"]
        db["alerts"].insert_one({"user": user_id, "msg": message})
        print(f"[Adapter] Logged notification to MongoDB alert collection.")
```

### Challenge 2: Transforming MVC into MVI State Flows
The following code snippet is structured as a basic Model-View-Controller script that alters state dynamically.

Refactor this code completely into a unidirectional Model-View-Intent (MVI) structure. Your refactored code must feature an immutable ```ThemeState```, a clear ```Intent``` class framework, and a single centralized state store processing dispatcher.

```python
# Current MVC implementation to be refactored
class ThemeModel:
    def __init__(self):
        self.mode = "LIGHT"  # Can be LIGHT, DARK, or HIGH_CONTRAST

class ThemeView:
    def display(self, mode: str):
        print(f"\n--- [SCREEN DISPLAY] Rendering UI with {mode} background theme ---")

class ThemeController:
    def __init__(self, model: ThemeModel, view: ThemeView):
        self.model = model
        self.view = view

    def toggle_dark_mode(self):
        if self.model.mode == "LIGHT":
            self.model.mode = "DARK"
        else:
            self.model.mode = "LIGHT"
        self.view.display(self.model.mode)

    def set_accessibility_mode(self):
        self.model.mode = "HIGH_CONTRAST"
        self.view.display(self.model.mode)

if __name__ == "__main__":
    m = ThemeModel()
    v = ThemeView()
    c = ThemeController(m, v)
    
    # Simulating UI events
    c.toggle_dark_mode()
    c.set_accessibility_mode()
```