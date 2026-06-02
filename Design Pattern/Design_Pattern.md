# Design Patterns
These are about how you structure code inside a single applicaiton (The Bricks) </br>
There are three types of patterns. They are - **Creational, Structural and Behavioral**

## Creational Patterns
These deals object creation mechanisms, trying to create objects in a manner suitable to the situation

***Singleton:** Ensures a class has only **one instance** and provides a global point of access to it. (e.g., a single Database Connection pool or a Configuration manager).
 ```python
 class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        # Initialize connection logic here
        return cls._instance
 ```

***Factory Method:** Provides an **interface** for creating objects but allows subclasses to alter the type of objects that will be created.
 ```python
 class Dog:
    def speak(self): return "Woof!"

 class Cat:
    def speak(self): return "Meow!"

 def pet_factory(pet_type="dog"):
    pets = {"dog": Dog, "cat": Cat}
    return pets[pet_type]() # Returns an instance
 ```

***Abstract Factory:** Lets you produce families of related objects without specifying their concrete classes.
 ```python
 class DarkButton:
    def render(self): return "Rendering Dark Button"

 class LightButton:
    def render(self): return "Rendering Light Button"

 class UIFactory:
    """The Abstract Factory"""
    def create_button(self): pass

 class DarkThemeFactory(UIFactory):
    def create_button(self): return DarkButton()

 class LightThemeFactory(UIFactory):
    def create_button(self): return LightButton()

 # Usage
 factory = DarkThemeFactory()
 button = factory.create_button()
 print(button.render())
 ```

***Builder:** Used to construct complex objects step-by-step. It’s great when an object has **10+ possible constructor parameters**.
 ```python
 class Computer:
    def __init__(self):
        self.ram = None
        self.gpu = None
        self.ssd = None

 class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def add_ram(self, size):
        self.computer.ram = size
        return self # Return self for chaining

    def add_gpu(self, model):
        self.computer.gpu = model
        return self

    def build(self):
        return self.computer

 # Usage
 pc = ComputerBuilder().add_ram("32GB").add_gpu("RTX 4090").build()
 ```

***Prototype:** Creates new objects by copying an existing object (cloning).
 ```python
 import copy

 class Prototype:
    def __init__(self):
        self.data = [i for i in range(1000)] # Expensive setup

    def clone(self):
        return copy.deepcopy(self)

 obj1 = Prototype()
 obj2 = obj1.clone()
 ```

### GOAL
How to create objects without creating a mess of dependencies.
| Pattern | Use Case | Pythonic Reality |
| :--- | :--- | :--- |
| **Singleton** | When you need exactly one instance (e.g., Config, Database). | Use a **Module**. In Python, modules are singletons by default. |
| **Factory** | When you don't know which class you'll need until runtime. | Use a **function** that returns a class instance. |
| **Builder** | When an object has a complex, multi-step setup. | Use **keyword arguments** or a dedicated Builder class for readability. |
| **Prototype** | When creating a new object is expensive. | Use `copy.deepcopy()`. |

## Structural Patterns
These deal with how classes and objects are composed to form larger structures.

***Adapter:** Acts as a wrapper between two incompatible interfaces. It's the "travel plug adapter" of the coding world.
 ```python
 class EuropeanSocket:
    def voltage(self): return 230

 class USASocketAdapter:
    def __init__(self, socket):
        self.socket = socket

    def request_110v(self):
        return self.socket.voltage() - 120 # "Adapting" the result

 # Usage
 euro_socket = EuropeanSocket()
 adapter = USASocketAdapter(euro_socket)
 print(f"Working at {adapter.request_110v()}V")
 ```

***Decorator:** Dynamically adds new behavior to an object without changing its implementation.
 ```python
 def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

 @log_call
 def my_function():
    print("Hello World")
 ```

***Facade:** Provides a simplified interface to a library, a framework, or any other complex set of classes.
 ```python
 class CPU:
    def freeze(self): print("Freezing CPU")
 class Memory:
    def load(self): print("Loading data")

 class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.mem = Memory()

    def start(self):
        self.cpu.freeze()
        self.mem.load()

 # Usage
 computer = ComputerFacade()
 computer.start() # One call instead of managing multiple objects
 ```

***Proxy:** Provides a placeholder for another object to control access to it (used for lazy loading or security).
 ```python
 class RealImage:
    def __init__(self):
        print("Loading heavy image from disk...")
    def display(self):
        print("Displaying image")

 class ProxyImage:
    def __init__(self):
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage() # Lazy Loading
        self._real_image.display()
 ```

### GOAL
How to assemble classes and objects into larger structures.

***Adapter:** Use this when you buy a 3rd-party library but its method names don't match your code. You wrap it in a class that "translates" the calls.

***Facade:** Use this when you have a complex system (like an authentication flow with 5 steps) and you want to give the user a single .login() button.

***Decorator:** Use this to add functionality (like logging or timing) without changing the original class. (Python’s @decorator is the gold standard here).

***Proxy:** Use this for "Lazy Loading." Don't load that 2GB ML model until the user actually clicks "Predict."

## Behavioral Patterns
These are specifically concerned with **communication between objects**.

***Observer:** A "subscription" mechanism to notify multiple objects about any events that happen to the object they’re observing. (The heart of MVC and Event-driven UI).
 ```python
 class NewsPublisher:
    def __init__(self):
        self._subscribers = []

    def attach(self, subscriber):
        self._subscribers.append(subscriber)

    def notify(self, message):
        for sub in self._subscribers:
            sub.update(message)

 # Usage: news_publisher.notify("Breaking News!")
 ```

***Strategy:** Defines a family of algorithms, puts each of them into a separate class, and makes their objects interchangeable.
 ```python
 def fedex_strategy(price): return price + 10
 def ups_strategy(price): return price + 5

 class Order:
    def __init__(self, price, shipping_strategy):
        self.price = price
        self.shipping_strategy = shipping_strategy

    def calculate_total(self):
        return self.shipping_strategy(self.price)

 # Usage
 order = Order(100, fedex_strategy)
 print(order.calculate_total())
 ```

***State:** Allows an object to alter its behavior when its internal state changes.
 ```python
 class State:
    def handle(self): pass

 class OnState(State):
    def handle(self): print("Light is already ON.")

 class OffState(State):
    def handle(self): print("Turning light ON...")

 class LightSwitch:
    def __init__(self):
        self.state = OffState()

    def press(self):
        self.state.handle()
        self.state = OnState() # Transition state
 ```

***Command:** Turns a request into a stand-alone object that contains all information about the request. This allows for "Undo" functionality.
 ```python
 class Light:
    def turn_on(self): print("Light ON")
    def turn_off(self): print("Light OFF")

 class Command:
    def execute(self): pass
    def undo(self): pass

 class TurnOnCommand(Command):
    def __init__(self, light):
        self.light = light
    def execute(self): self.light.turn_on()
    def undo(self): self.light.turn_off()

 # Usage
 remote = TurnOnCommand(Light())
 remote.execute()
 remote.undo()
 ```

 ***Memento:** This pattern is software's "Time Mechine". It allow to capture and restore the internal state of an object without violating **encapsulation**. The three pillars of Memento:
 1. Originator: it creates memento and knows how to restore itself from one.
 2. Memento: dumb object that stores the state. once created its data should not change
 3. Caretaker: it keeps history and holds the list of mementos but never modifies or even looks at what's inside them.

 ```python
import copy

class Memento:
    """The Immutable Snapshot"""
    def __init__(self, state):
        self._state = copy.deepcopy(state)
    def get_state(self):
        return self._state

class Originator:
    """The object that needs saving/restoring"""
    def __init__(self, state):
        self.state = state
    def save(self):
        return Memento(self.state)
    def restore(self, memento):
        self.state = memento.get_state()

class Caretaker:
    """The History Manager"""
    def __init__(self, originator):
        self._history = []
        self._originator = originator
    def backup(self):
        self._history.append(self._originator.save())
    def undo(self):
        if self._history:
            self._originator.restore(self._history.pop())
```

***Chains of Responsibility:** Passes a request along a chain of potential handlers. Each handler contains a reference to the next handler. It decides either to process the request or to pass it along the chain. This decouples the sender from the receiver.
```python
class Handler:
    """Abstract interface for handling requests"""
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class TechSupport(Handler):
    def handle(self, request):
        if request == "hardware":
            return "TechSupport: Fixed the hardware issue."
        return super().handle(request)

class BillingSupport(Handler):
    def handle(self, request):
        if request == "payment":
            return "BillingSupport: Processed the refund."
        return super().handle(request)
```

***Visitor:** If a new feature is needed in a group of objects, we use this pattern. It lets you add new operations to existing object structures without modifying the original classes. It uses a technique called Double Dispatch.

```python
class Place:
    def accept(self, visitor): pass

class House(Place):
    def accept(self, visitor): visitor.visit_house(self)

class Bank(Place):
    def accept(self, visitor): visitor.visit_bank(self)

class InsuranceVisitor:
    """The new functionality added without touching Place classes"""
    def visit_house(self, house):
        print("Calculating house insurance risk...")
    def visit_bank(self, bank):
        print("Calculating bank vault insurance risk...")
```

***Interpreter:** Defines a grammatical representation for a language and provides an interpreter to evaluate it. It represents each rule of the grammar as a class, making it easy to extend the language by adding new classes.
```python
class Expression:
    def interpret(self, context): pass

class Number(Expression):
    def __init__(self, value):
        self.value = value
    def interpret(self, context):
        return self.value

class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def interpret(self, context):
        return self.left.interpret(context) + self.right.interpret(context)

# Usage: Add(Number(5), Number(10)).interpret({}) -> 15
```
---
### GOAL
How objects communicate and distribute responsibility.

***Observer:** The "Pub/Sub" of code. When the User object changes, the UI and the Database both get notified automatically.

***Strategy:** Swap algorithms on the fly. Instead of a giant if/else block for "Shipping Method," pass the shipping function into the order.

***State:** Great for workflows. An Invoice object can behave differently depending on if its state is Unpaid, Processing, or Settled.

***Command:** Turns an action into an object. Essential if you want to implement Undo/Redo or a task queue.

## RuleBook of pattern choosing
Choosing a pattern is less about following a "rulebook" and more about identifying where your project's pain points will be in six months. If you pick a complex pattern for a simple script, you’ve over-engineered it; if you pick no pattern for a massive system, you’ve built a "spaghetti" monster.
<br> <br>
To choose correctly, you should evaluate these **five key parameters**.

1. The "Axis of Change"
Identify what is most likely to change in your project. Patterns are designed to "encapsulate" change so that when one thing moves, the rest stays still.

 * **If the Algorithm will change:** (e.g., switching from FedEx to UPS shipping) Use Strategy.

 * **If the Object Creation will change:** (e.g., adding new types of UI elements) Use Factory or Abstract Factory.

 * **If the Interface of a library will change:** Use Adapter.

 * **If the Steps of a process will change:** Use Template Method.

2. Complexity vs. Flexibility
There is a direct trade-off between how flexible a system is and how easy it is to read.

 * **Low Complexity (Scripts, Internal tools):** Avoid patterns. Use simple functions.

 * **Medium Complexity (Web Apps, APIs):** Use Facade to hide complexity and Decorators for cross-cutting concerns (logging, auth).

 * **High Complexity (Enterprise Engines, Game Loops):** Use Command, State, and Observer to decouple logic.

3. Direction of Data Flow
How do components talk to each other?

 * **One-to-Many:** If one object changes and ten others need to know about it, use Observer.

 * **Many-to-Many:** If you have dozens of objects talking to each other and it's becoming a mess, use Mediator to centralize the communication.

 * **Linear/Sequential:** If data passes through a series of stages, use Chain of Responsibility.

4. Lifecycle of Objects
How long do your objects need to live, and how are they born?

 * **Expensive Initialization:** If creating an object takes a lot of RAM or time, use Proxy (for lazy loading) or Prototype (for cloning).

 * **Global State:** If you truly need one single source of truth that never changes, use Singleton (though in Python, a module-level variable is usually better).

 * **Step-by-Step Construction:** If an object has many optional parts, use Builder.