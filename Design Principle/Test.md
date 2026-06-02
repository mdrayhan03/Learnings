# 🏅 Free Platforms to Test Your SOLID Principles Knowledge

Testing yourself on **SOLID principles** is a great way to measure how well you can spot code smells. While most dedicated technical assessment platforms (like Adaface or iMocha) are meant for corporate recruiters, there are excellent free courses on global learning platforms that offer **comprehensive tests, quizzes, and shareable certificates** upon completion.

---

## 🚀 Recommended Free Platforms with Certificates

### 1. Udemy (Free Tier Courses)
Udemy offers highly specific, short courses on software craftsmanship where you can watch brief refreshers and immediately take their module tests.
* **The Option:** Look for **"SOLID Design Principles"** or **"SOLID Principles"** by search filters set to *Price: Free*. 
* **What it includes:** Multiple-choice situational tests on spotting code violations (e.g., "Is this Square-Rectangle setup breaking LSP?").
* **Certificate:** You receive a downloadable Udemy Certificate of Completion when you finish all modules and quizzes.

### 2. Coursera (Financial Aid / Audit Track)
Coursera features deep, academic-grade testing on code architecture through major universities and tech organizations.
* **The Option:** Courses like **"Design Patterns"** (by University of Alberta) or language-specific design tracks.
* **How to get the Certificate Free:** Click on **"Financial Aid Available"** next to the Enroll button. Fill out the quick application, and Coursera almost always grants free access to the full track—including the graded assignments and the official certificate.
* **What it includes:** Actual refactoring assignments where your test submissions are evaluated against SOLID compliance.

---

## 📝 Practice Right Now: The Ultimate 5-Question SOLID Test

If you want to immediately gauge your understanding, try answering these real-world design scenarios based on our previous sessions. 

### Question 1: The Single Responsibility Principle (SRP)
> You have a `Report` class that calculates payroll data, formats it into a pretty HTML string, and emails it to the accounting team. To comply with SRP, how many total classes should this code be broken into?

### Question 2: The Open/Closed Principle (OCP)
> You have a `TaxCalculator` class with a method `calculate(item)`. Inside, there is an `if/else` block checking if the item is "Luxury", "Essential", or "Exported" to apply different tax rates. If you need to add a "Medical" item type, what action violates OCP, and what action satisfies it?

### Question 3: The Liskov Substitution Principle (LSP)
> You have a base class `ReadOnlyFile` with a method `read()`. You create a subclass `WritableFile` that adds a `write()` method. Does this violate the Liskov Substitution Principle? Why or why not?

### Question 4: The Interface Segregation Principle (ISP)
> You are building an interface for smart home devices called `SmartDevice`. It has methods: `turn_on()`, `turn_off()`, and `adjust_temperature()`. You try to implement this interface on a `SmartLightBulb` class. What is the design issue here according to ISP?

### Question 5: The Dependency Inversion Principle (DIP)
> A high-level class `OrderProcessor` directly instantiates `MySQLDatabase db = new MySQLDatabase()` inside its constructor to save orders. To invert this dependency, what structural change must you implement?

---

## 🎯 Scoring Guide
* **5/5 Correct:** Architect Level. You are ready to move directly into advanced architectural design patterns!
* **3/4 Correct:** Developer Level. You understand the theory well, but need to watch out for tricky edge cases (like inheritance traps).
* **1/2 Correct:** Student Level. A great start! Reviewing code smell definitions will help solidify the concepts.

## 📊 Test Results & Feedback
* **Q1 (SRP):** Perfect! Breaking it into ReportData, PayrollCalculator, HtmlFormatter, and EmailSender is exactly right. (And good catch, AccountingTeam would be the client or actor destination!).

* **Q2 (OCP):** Perfect! You correctly identified that adding another if/else breaks the "Closed for Modification" rule, and you instantly spotted the Strategy Pattern as the cure.

* **Q3 (LSP):** Perfect! This is a classic trick question. Many developers think adding new methods breaks LSP. It doesn’t! As long as a WritableFile can still be passed to any function expecting a ReadOnlyFile and read() works perfectly without throwing errors, LSP is safe.

* **Q4 (ISP):** Perfect! Forcing a lightbulb to implement adjust_temperature() is a textbook "fat interface" violation.

* **Q5 (DIP):** Perfect! Passing a generic Database abstraction/interface instead of hardcoding MySQLDatabase is exactly how you achieve Inversion of Control.

### 🎓 Your Score: 5/5 (Architect Level)

# 📝 Software Design Principles: Final Exam

### Question 1: Composition Over Inheritance
You are building a simulation game with vehicles like `Car`, `Boat`, and `AmphibiousCar` (which can drive on roads *and* float on water). 
* **A.** If you rely entirely on a strict, single-inheritance class tree, what structural nightmare do you run into?
* **B.** How does composition solve it?

---

### Question 2: Law of Demeter
You are reviewing a codebase and see this line inside an e-commerce order processor:  
`order.get_customer().get_address().get_zip_code().validate()`  

* **A.** Why does this line violate the Law of Demeter?  
* **B.** How would you rewrite the method invocation or interface to respect it?

---

### Question 3: KISS vs. YAGNI
Your team is tasked with building a feature that reads a basic `.csv` text file containing a list of usernames and prints them out. A developer submits a pull request with an entire, custom-built, asynchronous file-stream parsing engine that supports custom delimiters, character encoding detection, and parallel processing, saying *"We might need to process huge 5GB files later."* * **A.** Which design principles are violated here?  
* **B.** What is the proper, simpler solution for the current requirement?

---

### Question 4: Encapsulation
In Python, a developer creates a `User` class where a password string is stored as a standard public attribute (`self.password = "secret123"`). 

* **A.** Why does this break the core concept of encapsulation?  
* **B.** What features or decorators does Python provide to clean this up and protect the internal state?

---

### Question 5: Fail Fast
Look at the nested code block below:

```python
def process_payment(user, amount):
    if user is not None:
        if amount > 0:
            if user.has_active_card():
                # Core logic: charge the card
                return True
    return False
```
How would you refactor this method to adhere to the Fail Fast principle using Guard Clauses?

# 🎓 Final Exam Evaluation Report
You did a fantastic job analyzing these real-world architectural issues. Let's grade your answers line by line to see exactly how your structural understanding holds up under pressure.

## 📊 Detailed Breakdown & Feedback
### 🚗 Q1: Composition Over Inheritance (Score: 4.5 / 5)
Your Answer (A): Correct on the downside! If you modify or update features in a parent class, you risk breaking child classes across the entire system. To add a specific structural detail: with single inheritance, an AmphibiousCar would be forced to inherit from either Car or Boat, missing out on the other's methods, leading to massive copy-pasted code or a messy hierarchy.

Your Answer (B): Spot on. By passing driving or floating features as injected component references, you avoid rigid subclass hierarchies entirely.

### 🚊 Q2: Law of Demeter (Score: 4.5 / 5)
Your Answer (A): Exactly right! order is heavily coupled to things it shouldn't know anything about (like the internal setup of the address and zip code objects). If the ZipCode class changes its layout, your OrderProcessor breaks.

Your Answer (B): Good intuition on routing dependencies only to the immediate next class. To write this strictly in clean code, you would reduce the invocation entirely by delegating the work downward, letting the order just talk to the customer:

```python
# From this trainwreck:
order.get_customer().get_address().get_zip_code().validate()

# To this clean LoD invocation:
order.validate_shipping_destination()
```

### 📉 Q3: KISS vs. YAGNI (Score: 5 / 5)
Your Answer: A perfect assessment. The developer completely violated YAGNI by building out features for hypothetical future files that do not exist today. Your solution is pure KISS: just drop in standard Python built-in tools (like import csv) to do the direct task clearly and simply.

### 🔐 Q4: Encapsulation (Score: 5 / 5)
Your Answer: Textbook definition. Storing sensitive variables like a password out in the open allows rogue scripts or accidental typos to overwrite them directly. Using Python's _password naming convention combined with @property and @password.setter restores absolute control over how data is processed, validated, or read.

### ⚡ Q5: Fail Fast Refactoring (Score: 5 / 5)
Your Code: Flawless! Let's look at how much cleaner your version is compared to the original:

```python
# Your Refactored Code - Clean, flat, and highly readable
def process_payment(user, amount):
    if user is None:
         return False
    if amount <= 0:
        return False
    if not user.has_active_card():
        return False
        
    # core logic
    return True
```
You successfully systematically flipped every condition to catch error states at the front gate, returning early and keeping the core happy path entirely unindented at the bottom.

## 🏆 Final Score: 23 / 25 — ARCHITECT GRADUATE!