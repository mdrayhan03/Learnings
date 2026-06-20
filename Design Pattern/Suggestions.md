## 🚀 Design Patterns Mastery Roadmap

| Pattern Category | Design Pattern | Practice Mini-Project Idea | The "Hands-on" Challenge | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Creational** | **Singleton** | Database Connection Manager | Ensure only one connection instance exists across your entire app, even with multiple threads. | ✅ **Done** |
| *(Focus on creation)* | **Factory Method** | Cross-Platform UI Button Creator | Create a system that returns a `WindowsButton` or `MacButton` based on the OS without the client knowing the class. | ✅ **Done** |
| | **Abstract Factory** | Dark/Light Mode Theme Kit | Generate a whole family of related objects (Buttons, Checkboxes, Sliders) that all match a specific "Style." | ✅ **Done** |
| | **Builder** | Custom Pizza or Burger Order | Build a complex object with many optional parts (toppings, sauces, crust types) using a step-by-step API. | ✅ **Done** |
| | **Prototype** | Game Character Spawner | Create an "Enemy" template and clone it 100 times with slight variations in position instead of calling `new Enemy()` repeatedly. | ✅ **Done** |
| --- | --- | --- | --- | --- |
| **Structural** | **Adapter** | Legacy Printer Connector | Make a modern JSON data source work with an old library that only accepts XML input. | ✅ **Done** |
| *(Focus on composition)*| **Bridge** | Remote Control & Device System | Separate the "Remote Control" logic (buttons) from the "Device" logic (TV, Radio) so they can vary independently. | ✅ **Done** |
| | **Composite** | File System Directory | Treat individual Files and Folders (which contain files) as the same type so you can "Calculate Size" on both. | ✅ **Done** |
| | **Decorator** | Text Formatter | Take a "Plain Text" object and dynamically wrap it with `BoldDecorator`, `ItalicDecorator`, or `UnderlineDecorator`. | ✅ **Done** |
| | **Facade** | Home Theater "One-Button" Start | Create one class that handles the complex sequence of turning on the TV, Soundbar, and DVD Player at once. | ✅ **Done** |
| | **Proxy** | Image Gallery Caching | Create a placeholder object that only loads a heavy high-res image from "disk" when it's actually scrolled into view. | ✅ **Done** |
| --- | --- | --- | --- | --- |
| **Behavioral** | **Strategy** | E-commerce Checkout | Switch between different payment methods (PayPal, Credit Card, Crypto) at runtime using the same `pay()` method. | ✅ **Done** |
| *(Focus on communication)*| **Observer** | YouTube/Newsletter Subscription | Create a "Subject" (Creator) that automatically notifies all "Observers" (Subscribers) when a new video is posted. | ✅ **Done** |
| | **Command** | Smart Home Undo/Redo | Represent "Turn on Light" as an object so you can store it in a list and "Undo" the last 5 actions. | ✅ **Done** |
| | **State** | Vending Machine Logic | Change how the machine reacts to "Press Button" based on whether it is in the `NoCoin`, `HasCoin`, or `OutOfStock` state. | ✅ **Done** |
| | **Template Method** | Data Miner / Parser | Define a standard skeleton for "Read Data -> Process -> Save," but let subclasses decide how to read from CSV vs. PDF. | ✅ **Done** |
| | **Iterator** | Social Media Feed | Create a custom way to loop through a collection of "Posts" (e.g., skip ads, only show friends) without exposing the list. | ✅ **Done** |
| | **Memento** | Video Game "Save Point" | Capture a `PlayerState` (HP, Level) and store it so you can "Undo" a character's death without breaking encapsulation. | ✅ **Done** |
| | **Chain of Responsibility** | Support Ticket System | Pass a request through a chain: `Level1Tech` -> `Manager` -> `CEO`. Each handler decides to solve it or pass it on. | ✅ **Done** |
| | **Visitor** | Insurance Risk Calculator | Add new operations (like `calculate_tax`) to a group of objects (Building, Car) without changing their classes. | ✅ **Done** |
| | **Interpreter** | Custom Math Parser | Define a grammar for a simple language (e.g., "5 PLUS 2") and evaluate it using a tree of expressions. | ✅ **Done** |

