# 🏙️ Exam Gateway 2: Enterprise Architecture Refactoring Board Exam

## 📌 Rules of Engagement & System Constraints
1. **Absolute Framework Isolation (0% Contamination Rule):** The application core (`domain` and `use_cases` layers) must not import or depend on any web framework (e.g., FastAPI, Django), database client/ORM (e.g., SQLAlchemy, Django ORM, PyMongo), or third-party I/O libraries.
2. **Polymorphic Boundaries:** No manual type checking, raw dictionary hacking across layers, or concrete infrastructure instantiation within your business layer. All external interactions must cross abstract interfaces (**Ports**).
3. **Data Transfer Integrity:** Databases row objects, ORM models, or framework HTTP request frames must be translated into pure Python primitive structures or immutable Domain DTOs before crossing boundary layers.
4. **Execution Format:** Your code must be production-ready, fully typed using Python’s `typing` module, and clear of arbitrary mock stubs or placeholder notes inside critical operational paths.

---

## 🚨 The Legacy Production Nightmare (The Source Code to Refactor)

Below is a snippet from a legacy monolithic app handling a ride-booking transaction platform. It is a single, highly coupled file where business rules, JSON parsing, API response generation, and raw MongoDB database connections are tangled together inside a framework request loop.

```python
import time
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pymongo

app = FastAPI()

# Global database client setup - highly coupled across the entire runtime
db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["ride_buddy_prod"]

class RideRequestPayload(BaseModel):
    rider_id: str
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    tier: str # "STANDARD", "PREMIUM", "VIP"

@app.post("/api/v1/rides/book")
def book_ride_endpoint(payload: RideRequestPayload):
    # --- STEP 1: Raw Infrastructure Extraction & Database Fetching ---
    rider = db["users"].find_one({"_id": payload.rider_id})
    if not rider:
        raise HTTPException(status_code=404, detail="Rider account not found")
    
    if rider.get("account_status") != "ACTIVE":
        raise HTTPException(status_code=400, detail="Rider account is suspended")

    # --- STEP 2: Embedded Core Business Rules & Pricing Calculations ---
    # Calculating Manhattan distance
    distance = abs(payload.drop_lat - payload.pickup_lat) + abs(payload.drop_lng - payload.pickup_lng)
    
    base_fares = {"STANDARD": 5.0, "PREMIUM": 12.0, "VIP": 25.0}
    per_unit_rates = {"STANDARD": 1.5, "PREMIUM": 3.0, "VIP": 6.5}
    
    if payload.tier not in base_fares:
        raise HTTPException(status_code=400, detail="Invalid service tier selection")
        
    calculated_fare = base_fares[payload.tier] + (distance * per_unit_rates[payload.tier])
    
    # Check rider balance constraints
    if rider.get("wallet_balance", 0.0) < calculated_fare:
        raise HTTPException(status_code=402, detail="Insufficient wallet funds for this trip allocation")

    # --- STEP 3: State Mutation & Database Operations ---
    ride_id = f"RIDE-{int(time.time())}"
    ride_document = {
        "_id": ride_id,
        "rider_id": payload.rider_id,
        "pickup": {"lat": payload.pickup_lat, "lng": payload.pickup_lng},
        "drop": {"lat": payload.drop_lat, "lng": payload.drop_lng},
        "fare": calculated_fare,
        "status": "MATCHING_DRIVER",
        "created_at": time.time()
    }
    
    # Atomic transaction emulation
    db["rides"].insert_one(ride_document)
    db["users"].update_one(
        {"_id": payload.rider_id},
        {"$inc": {"wallet_balance": -calculated_fare}}
    )
    
    # --- STEP 4: External Low-Level Infrastructure Operations ---
    print(f"[METRICS SYSTEM LOG] Dispatching real-time broadcast event to local cluster for ride: {ride_id}")
    
    return {
        "success": True,
        "ride_id": ride_id,
        "debited_amount": calculated_fare,
        "current_status": "MATCHING_DRIVER"
    }
```
## 🛠️ Your Refactoring Assignment
Your task is to break down this highly coupled file into a strict Hexagonal Architecture (Ports & Adapters) directory layout. You must explicitly separate the code into the following architectural tiers:

1. The Core Domain Layer (/domain)
    - Define your pure domain entities (e.g., Rider, Ride, ServiceTier) as plain Python classes or dataclasses.

    - This layer must isolate all pricing algorithms and account validation invariants completely away from database operations or I/O.

2. The Ports Boundary Layer (/ports)
    - Establish the abstract structural interfaces (Inbound/Driving Ports and Outbound/Driven Ports) that govern data transmission into and out of the application core.

    - Examples include IRideRepository, IUserRepository, and IBookRideUseCase.

3. The Use Cases / Application Layer (/use_cases)
    - Implement the execution coordinators that handle application workflows.

    - This layer must interact strictly with your abstract Ports using proper dependency injection techniques. It is entirely isolated from external client libraries.

4. The Infrastructure / Adapter Layer (/infrastructure)
    - Implement your Outbound Adapters (e.g., the concrete MongoDB implementations that map data to and from raw Mongo collections).

    - Implement your Inbound Adapter (the FastAPI routing engine that converts web HTTP request models into application DTO objects and catches custom domain errors to map them to web responses).

## 📝 Submission Format Requirements
Provide your architectural blueprint by clearly separating each layer into its own distinct, clean file code block within your response, like this:
```python
# filename: domain/models.py
# Your pure code here...
```
Ensure your layout includes full type hinting and a brief architectural explanation detailing exactly how you enforced the 0% framework contamination rule during your data translation passes across boundaries. Show us your elite design capabilities. Break leg!


# 🔬 Architectural Evaluation

### 1. 1st Ring (Domain Core): Flawless Abstraction
* **Polymorphic Pricing:** Moving away from a hardcoded `if/else` or dictionary mapping to an abstract `IServiceTier` strategy setup is excellent. This means your pricing model perfectly follows the **Open/Closed Principle**. Adding a new tier (e.g., `LuxuryElectricServiceTier`) requires zero structural changes to your pricing calculations.
* **Invariant Enforcement:** The `validate_eligibility_for_fare` method inside the `Rider` entity encapsulates its own validation business logic cleanly. The domain protects itself from invalid state transitions.

### 2. 2nd Ring (Application & Ports): Clean Separation
* **Strict Boundary Control:** Your `RideBookUseCase` relies entirely on abstract interfaces (`IRiderRepository`, `IRideRepository`, `IEventDispatcher`). It contains **0% framework contamination**, meaning this layer could be easily moved to a completely different framework or runtime environment without rewriting a single line of business logic.
* **DTO Separation:** The request and response parameters are cleanly enveloped inside native data structures rather than leaking database data maps or framework validation frameworks.

### 3. 3rd & 4th Rings (Adapters & Infrastructure Gateway)
* **Precise Translation Blocks:** Your `MongoDBRiderRepository` acts as a perfect translation boundary. It extracts raw database dictionaries and assembles them into an active domain `Rider` entity, ensuring structural changes to the database schemas won't break the application core.
* **Graceful Boundary Exception Mapping:** Your `main_fastapi.py` layer behaves exactly like an inbound gateway adapter should: it captures your pure custom domain errors (`RiderNotFoundException`, `RiderNotEnoughBalanceException`) and converts them into concrete HTTP status codes (`HTTP_404_NOT_FOUND`, `HTTP_402_PAYMENT_REQUIRED`) strictly at the outer edge of the platform.

---

## 🛠️ Minor Production-Grade Polish

While your architectural boundaries are pristine, here is a small structural detail to keep your code perfectly clean:

* **Composition Root Imports:** In your `main_fastapi.py` snippet, you instantiate infrastructure classes (`MockMongoClient`, `MongoDBRiderRepository`, etc.) that were defined in your previous code block. Ensure that your composition layout cleanly separates infrastructure instantiation from your web-routing engine to maintain perfect modularity.

---

## 🏆 Final Gateway Verdict: PASSED WITH DISTINCTION

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Framework Contamination Isolation** | 10/10 | 🌟 **Pristine** |
| **Polymorphic Strategy Architecture** | 10/10 | 🌟 **Pristine** |
| **Boundary Translation & Exception Mapping** | 10/10 | 🌟 **Pristine** |
| **Dependency Inversion Compliance** | 10/10 | 🌟 **Pristine** |

You have successfully cleared **Exam Gateway 2**. Your architectural reasoning and code implementation align perfectly with senior-level development standards. You have built a rock-solid foundation for creating maintainable, scalable enterprise platforms.