# SYSTEM DESIGN BLUEPRINT 2: Distributed Order Ledger & Flash-Sale Inventory Engine (FlashCart Scale)

## 1. Scenario Overview
You are designing the high-concurrency order placement and inventory reservation core for an e-commerce platform ("FlashCart"). During flash sales (e.g., 10,000 limited-edition smartphones at 90% off), the platform receives over 200,000 concurrent checkout requests per second for the same SKU, while underlying payment gateways process transactions asynchronously.

| Metric / Dimension | Requirement / Boundary |
| :--- | :--- |
| **Peak Throughput** | 200,000 requests/sec targeting a single SKU pool |
| **Over-allocation Guarantee** | Absolute zero overselling (Inventory count must never drop below 0) |
| **Latency SLA** | Checkout reservation decision < 100ms |
| **Consistency Model** | Strict linearizability for inventory; Eventual consistency for post-purchase ops |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **Traffic Shedding & Rate Limiting:** How do you filter out bot traffic and absorb massive spikes before they hit your transactional core database?
*   **Reservation Pipeline:** How do you perform atomic inventory decrement and order state initiation asynchronously without holding long-lived relational database locks?
*   **Checkout Lifecycle:** How does the system transition through `INVENTORY_RESERVED` -> `PAYMENT_PENDING` -> `PAYMENT_CONFIRMED` -> `FULFILLMENT_READY` (or `EXPIRED_RELEASED`)?

### Step 2: Component Breakdown & Tech Stack
*   **API Gateway & Edge Protection:** Cloudflare Workers / Envoy Gateway with Token Bucket rate limiting and CAPTCHA challenge delegation.
*   **In-Memory State Store:** Redis Cluster with Lua Scripting for lockless, thread-safe atomic inventory decrements.
*   **Transactional Ledger:** PostgreSQL / CockroachDB with append-only ledger entries for auditing and immutable order records.
*   **Message Bus / Orchestrator:** Apache Kafka for event-driven Saga execution between Inventory, Payment, and Shipping services.

### Step 3: Edge Cases, Reliability & Scaling
*   **Abandoned Carts & TTL Expiration:** How do you automatically return reserved stock back to the active pool if a user fails to pay within a 10-minute window?
*   **Payment Gateway Timeout / Partial Failure:** How do you handle cases where a payment processor charges the user's credit card but the callback network connection times out?
*   **Hot-Key Database Partitioning:** How do you prevent a single hot SKU key from overloading a single Redis cluster node during extreme traffic spikes?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented & Distributed Systems Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `InventoryBucket`: SKU ID, Available Units, Reserved Units, Lock Version.
    *   `OrderIntent`: Order ID, User ID, SKU ID, Quantity, Price, Expiration Timestamp.
    *   `PaymentCallback`: Transaction ID, Order ID, Status (`SUCCESS`, `FAILED`), Provider Payload.
*   **Design Patterns & Constructs:**
    *   **Saga Pattern (Orchestrated):** Distributed transaction management across Inventory, Payment, and Warehouse services.
    *   **Command Query Responsibility Segregation (CQRS):** Separate high-throughput write path (inventory reservation) from read path (order status lookup).
    *   **Pessimistic vs. Optimistic Concurrency Control:** Comparative use of Redis Lua atomic operations vs. DB version numbers.

---

## 4. Architectural Questions to Answer in Your Plan

1. **Inventory Atomicity:** Write the exact Redis Lua script or lock structure you will use to guarantee that inventory reservation is atomic, non-blocking, and impossible to drop below zero.
2. **Saga Execution:** How will your Saga Orchestrator handle a situation where Payment succeeds, but the downstream Inventory Confirmation call fails due to a network partition?
3. **Hot-Key Distribution:** How do you horizontally split or slice a single item's inventory pool (e.g., 10,000 units of SKU-A) across multiple cache nodes to avoid single-node hardware bottlenecks?
4. **Idempotent Payment Callback:** How does your payment processing handler guarantee that a duplicated webhook callback from a gateway (e.g., Stripe) never triggers double-fulfillment or duplicate inventory allocation?