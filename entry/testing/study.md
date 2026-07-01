# PyTest Syntax & Feature Reference Guide

## 1. Basic Assertions
PyTest uses standard Python comparison operators instead of custom methods.

```python
def test_basic_assertions():
    assert 5 + 5 == 10              # Equality
    assert "qa" in "qa_engineer"    # Substring check
    assert True is not False        # Identity / Boolean
    assert [1, 2] != [3, 4]         # Inequality
```

## 2. Testing Expected Exceptions
Use pytest.raises to ensure your code throws the correct error when given bad data.
```python
import pytest

def test_value_error_raised():
    with pytest.raises(ValueError) as exc_info:
        int("not_a_number")
    
    # Optional: Verify the exact error message text
    assert "invalid literal for int()" in str(exc_info.value)
```

## 3. Fixtures (Setup & Teardown)
Fixtures handle preparing resources before a test and cleaning them up afterward using the yield keyword.
```python
import pytest

@pytest.fixture(scope="function") # Scopes: function, class, module, session
def sample_data():
    # --- SETUP CODE ---
    data = {"id": 101, "role": "admin"}
    print("\nSetting up test data...")
    
    yield data  # Injects this object into the test function
    
    # --- TEARDOWN CODE ---
    print("\nCleaning up test data...")
    data.clear()

def test_user_role(sample_data):
    assert sample_data["role"] == "admin"
```

## 4. Parameterized Tests (Data-Driven Testing)
Instead of copying a test multiple times for different inputs, use @pytest.mark.parametrize to pass a list of inputs into a single test function.
```python
import pytest

@pytest.mark.parametrize("inputs, expected_output", [
    ((2, 3), 5),   # Run 1: 2 + 3 = 5
    ((0, 0), 0),   # Run 2: 0 + 0 = 0
    ((-1, 5), 4),  # Run 3: -1 + 5 = 4
])
def test_addition(inputs, expected_output):
    num1, num2 = inputs
    assert num1 + num2 == expected_output
```

## 5. Test Markers (Filtering & Organization)
You can tag tests with custom labels to group them, or use built-in markers like skip and xfail (expected failure).
```python
import pytest

@pytest.mark.smoke
def test_critical_login_path():
    assert True

@pytest.mark.skip(reason="Jira ticket #1043: Feature currently broken in dev")
def test_legacy_report():
    assert False

@pytest.mark.xfail(reason="We know this API endpoint is down right now")
def test_flaky_third_party_api():
    assert False
```

## 6. Essential Terminal Execution Commands
Run these commands from your terminal root folder to control how PyTest executes:
```python
# Run all tests found in the current directory and subdirectories
pytest

# Verbose mode (shows exact names of passing/failing tests)
pytest -v

# Print statements (don't hide print output inside tests)
pytest -s

# Run tests matching a specific file name
pytest test_login.py

# Run only tests tagged with a specific marker (e.g., smoke)
pytest -m smoke

# Stop execution immediately after the first failure occurs
pytest -x

# Run only a specific test function inside a specific file
pytest test_login.py::test_critical_login_path
```

---
---

# Comprehensive Python QA Automation Blueprint
### Master Reference Guide: API Testing, UI Automation, and Global Architecture

This production-ready reference documentation outlines the complete architecture, layout, design patterns, and deployment configurations required to build a professional-grade test suite covering both **Backend APIs** and **Frontend Web UIs** using Python, PyTest, Playwright, and Requests.

---

## 1. Directory Structure Architecture
A scalable test automation framework separates configurations, backend API clients, frontend page object abstractions, and actual verification tests into distinct layers.

```text
my_automation_framework/
│
├── conftest.py               # Global testing lifecycle, setups, and shared fixtures
├── requirements.txt          # Explicit package version lockfile
│
├── pages/                    # The UI Abstraction Layer (Page Object Model)
│   ├── __init__.py           # Makes the folder an importable Python module
│   └── login_page.py         # Locators and structural interactions for the UI
│
└── tests/                    # The Verification Layer (Business Logic Assertions)
    ├── __init__.py           # Makes tests discoverable
    ├── test_api_backend.py   # Backend API Automated Tests
    └── test_ui_frontend.py   # Frontend UI Automated Tests
```

## 2. Dependency Management (requirements.txt)
To ensure your framework runs identically across local machines, Docker environments, and CI/CD runners, freeze your dependencies to explicit production versions.
```
Plaintext
pytest==8.2.1
pytest-playwright==0.5.0
requests==2.32.3
```
To initialize your environment, execute: pip install -r requirements.txt && playwright install

## 3. Global Configuration & Shared Lifecycle (conftest.py)
This file handles the heavy lifting of the framework. Any fixture defined here is automatically shared globally with every single test file in that directory—without needing a single import statement.

```python
# conftest.py
import pytest
import requests
from playwright.sync_api import sync_playwright

# ==========================================
# 1. GLOBAL API AUTOMATION CONFIGURATIONS
# ==========================================
@pytest.fixture(scope="session")
def api_base_url():
    """Provides a centralized, global base URL for API test configurations."""
    return "[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)"


# ==========================================
# 2. GLOBAL UI/BROWSER CONFIGURATIONS
# ==========================================
@pytest.fixture(scope="session")
def browser_instance():
    """
    Initializes and manages the core browser engine background process.
    Runs exactly once per test session to optimize memory usage.
    """
    print("\n[GLOBAL HOOK] Spinning up underlying browser engine...")
    playwright_driver = sync_playwright().start()
    
    # Set headless=True for faster execution on remote Linux cloud environments
    monitored_browser = playwright_driver.chromium.launch(headless=False)
    
    yield monitored_browser  # Pass resource to downstream dependencies
    
    print("\n[GLOBAL HOOK] Tearing down browser engine safely...")
    monitored_browser.close()
    playwright_driver.stop()


@pytest.fixture(scope="function")
def context_tab(browser_instance):
    """
    Creates an isolated, pristine browser context and tab for every UI test.
    Ensures zero cross-test cookie, session, or cache contamination.
    """
    print("\n[TEST SETUP] Instantiating isolated session tab...")
    isolated_context = browser_instance.new_context()
    active_page = isolated_context.new_page()
    
    yield active_page  # Inject active browser tab directly into UI test scripts
    
    print("\n[TEST TEARDOWN] Terminating session tab and clearing cache...")
    active_page.close()
    isolated_context.close()
```

## 4. The UI Abstraction Layer: Page Object Model (pages/login_page.py)
This class forms an abstraction shield around web page elements. It contains all the CSS/Data selector paths and core interactions, meaning test files don't need to know anything about raw HTML structures.

```python
# pages/login_page.py
from playwright.sync_api import Page, Locator

class LoginPage:
    def __init__(self, page: Page):
        """Maps out the page elements and binds them to the active context tab."""
        self.page = page
        self.target_url = "[https://www.saucedemo.com/](https://www.saucedemo.com/)"
        
        # Industry Best Practice: Leverage isolated attributes rather than volatile text paths
        self.username_field: Locator = page.locator("[data-test='username']")
        self.password_field: Locator = page.locator("[data-test='password']")
        self.submit_button: Locator = page.locator("[data-test='login-button']")
        self.error_container: Locator = page.locator("[data-test='error']")

    def open_application(self) -> None:
        """Navigates the browser instance to the login interface target."""
        self.page.goto(self.target_url)

    def execute_login_workflow(self, user_string: str, password_string: str) -> None:
        """Encapsulates string input typing and click interaction workflows."""
        self.username_field.fill(user_string)
        self.password_field.fill(password_string)
        self.submit_button.click()

    def capture_error_feedback(self) -> str:
        """Extracts text content string properties emitted inside the error element."""
        return self.error_container.text_content() or ""
```

## 5. Backend Verification Layer (tests/test_api_backend.py)
This file leverages the requests library combined with PyTest parameters to test REST API endpoints rapidly with data-driven variations.

```python
# tests/test_api_backend.py
import pytest
import requests

def test_get_specific_post_matches_schema(api_base_url):
    """Test a GET request to fetch post #1 and validate its contents."""
    response = requests.get(f"{api_base_url}/posts/1")
    response_data = response.json()
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response_data["id"] == 1
    assert "title" in response_data
    assert isinstance(response_data["userId"], int)


@pytest.mark.parametrize("payload, expected_status", [
    ({"title": "Valid Post", "body": "Hello World", "userId": 1}, 201),
    ({"title": "", "body": "", "userId": 1}, 201),
    ({"title": "Edge Case", "body": "Testing IDs", "userId": 999999}, 201)
])
def test_create_post_payloads(api_base_url, payload, expected_status):
    """Data-driven testing verifying endpoint payload validation restrictions."""
    response = requests.post(f"{api_base_url}/posts", json=payload)
    
    assert response.status_code == expected_status
    if response.status_code == 201:
        assert response.json()["title"] == payload["title"]
```

## 6. Frontend Verification Layer (tests/test_ui_frontend.py)
This module houses the business assertions for your UI. It relies on custom PyTest marks to pipe data variations through the page object model abstraction layer.

```python
# tests/test_ui_frontend.py
import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.parametrize("bad_user, bad_password, expected_validation_error", [
    ("unregistered_entity", "secret_pass", "Username and password do not match any user"),
    ("standard_user", "", "Password is required"),
    ("", "secret_sauce", "Username is required")
])
def test_authentication_error_flows(context_tab, bad_user, bad_password, expected_validation_error):
    """
    Executes multiple UI authentication checks using parametrized inputs.
    Notice that no framework imports are needed for 'context_tab'—PyTest links it from conftest.py.
    """
    # 1. Initialize Page Object Model layer using shared fixture hook
    login_screen = LoginPage(context_tab)
    
    # 2. Perform the target system actions
    login_screen.open_application()
    login_screen.execute_login_workflow(bad_user, bad_password)
    
    # 3. Assert target response values meet expected criteria
    actual_error = login_screen.capture_error_feedback()
    assert expected_validation_error in actual_error, f"Expected message missing. Found: '{actual_error}'"
```

## 7. Execution Command Reference
Run these variations within your project root folder to control framework execution paths:

```bash
# Execute entire test engine variations silently (Default Headless mode)
pytest

# Execute in Headed Desktop GUI mode with explicit console print output visible
pytest -v -s

# Execute target test procedures filtering explicitly by tag markers
pytest -m smoke

# Execute only backend API tests
pytest tests/test_api_backend.py -v

# Instantly halt the entire pipeline operation upon encountering the first failure point
pytest -x
```

---
---
---

# Advanced QA Engineering Learning Checklist & Todo Guide
### Phase 3 & 4: DevOps, Infrastructure, and Non-Functional Automation Architecture

This master checklist serves as your advanced educational roadmap. Check off each milestone as you progress from writing local test scripts to architecting distributed, enterprise-grade testing infrastructures.

---

## 🏁 Milestone 1: CI/CD Pipeline Automation (DevOps)
*Goal: Stop running tests manually. Automate execution on every code change.*

- [ ] **Task 1: Master Git Workflows**
  - Learn branch isolation (`git checkout -b feature/test-suite`), committing, and opening Pull Requests (PRs).
  - Understand how to handle merge conflicts within your test code.

- [ ] **Task 2: Build a GitHub Actions Workflow Pipeline**
  - Create a `.github/workflows/run-tests.yml` configuration file in your project root.
  - Automate the environment setup to trigger tests on every `git push` or `pull_request`.
  - *Example Core Pipeline Structure:*
    ```yaml
    name: Regression Suite
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Set up Python
            uses: actions/setup-python@v5
            with: {python-version: '3.11'}
          - name: Install Dependencies
            run: |
              pip install -r requirements.txt
              playwright install chromium
          - name: Execute PyTest Automation
            run: pytest tests/ --headless
    ```

- [ ] **Task 3: Containerize the Testing Environment with Docker**
  - Write a production `Dockerfile` to bundle Python, framework dependencies, and headless browser drivers into a single isolated block.
  - Eliminate the "it works on my machine" problem entirely across the engineering team.

---

## 📊 Milestone 2: Non-Functional Testing (Performance & Security)
*Goal: Ensure the system is fast, secure, and doesn't crash under stress.*

- [ ] **Task 1: Load Testing with Locust (Python-Based)**
  - Use `pip install locust` to write performance scripts entirely in Python.
  - Simulate thousands of concurrent virtual users (`HttpUser`) hitting backend API endpoints simultaneously.
  - Identify response time degradation, throughput limits, and server breaking points.
  - *Example Performance Script Syntax:*
    ```python
    from locust import HttpUser, task, between

    class StressTestUser(HttpUser):
        wait_time = between(1, 3) # Simulate real human delays

        @task
        def check_catalog_performance(self):
            self.client.get("/posts")
    ```

- [ ] **Task 2: Security Automation & Vulnerability Scanning**
  - Study the **OWASP Top 10** standard reference document (SQL Injection, Cross-Site Scripting, Broken Auth).
  - Integrate automated application vulnerability scanners like **OWASP ZAP** or `safety`/`bandit` (Python code scanning packages) directly into your CI/CD pipelines.

---

## 💾 Milestone 3: Advanced Data & Integration Automation
*Goal: Connect directly to databases and isolate external application dependencies.*

- [ ] **Task 1: Database Verification (DB Testing Layer)**
  - Use database connector libraries like `SQLAlchemy` or `psycopg2` inside custom PyTest fixtures.
  - **The E2E Pattern:** Perform an event on the UI frontend (e.g., registering an account), then immediately write an automated SQL query directly to the database to ensure the row parameters match on disk.
  - *Example Backend DB Connection Pattern:*
    ```python
    @pytest.fixture
    def db_cursor():
        connection = psycopg2.connect(dsn="your_connection_string")
        cursor = connection.cursor()
        yield cursor
        cursor.close()
        connection.close()
    ```

- [ ] **Task 2: Mocking and API Service Virtualization**
  - Master Python's native `unittest.mock` engine and the `pytest-mock` plugin wrapper.
  - Intercept out-of-system network transactions (like paid Stripe Payment Gateways, SMS text dispatch paths, or unstable third-party data APIs).
  - Force mock responses to instantly simulate hard-to-test scenarios like credit card rejections, network timeouts, or server 500 crashes.

---

## 📈 Career Checkpoint: The Professional SDET Target Matrix

| Architectural Milestone | Local Beginner State | Industry Professional Target |
| :--- | :--- | :--- |
| **Execution Trigger** | Manual terminal input via desktop | Completely event-driven via **CI/CD Triggers** |
| **Runtime Isolation** | Local host system state dependency | Lightweight, isolated **Docker Containers** |
| **Scaling Capability** | Serial execution on one machine | Parallel multi-threaded execution scaling via cloud nodes |
| **Data Verification** | Superficial visual screen verification | End-to-end processing verification directly in **Databases** |