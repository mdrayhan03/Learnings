# FoodDash System Design Blueprint: Real-Time Notification Engine

## 1. Scenario Overview

You are leading the engineering effort for **FoodDash**, a rapidly growing food delivery app. The product team wants to launch a complete notification engine serving three core features with distinct operational profiles:

| Feature | Primary Triggers | Target Channels | SLA & Priority |
| :--- | :--- | :--- | :--- |
| **Feature A: Order Updates** | `ORDER_PLACED`, `PREPARING`, `OUT_FOR_DELIVERY`, `DELIVERED` | Push, In-App, Email (receipt) | High Priority, Real-time |
| **Feature B: Account Security & Auth** | Password Reset, 2FA Code, Unknown Login | SMS, Email | Critical Priority, SLA < 3s (Bypasses Opt-outs) |
| **Feature C: Promotional Campaigns** | Flash Sales, Geo-targeted Discounts | Push, Email | Low Priority, Massive Batch (Quiet hours & Rate-limited) |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **Ingestion Layer:** How do the 3 FoodDash backend services publish notification requests?
*   **Routing & Filtering:** Where do template hydration, quiet hours checking, and user opt-out validation take place?
*   **Queue Topology:** How are messages partitioned across queues (e.g., dedicated queues for High/Critical vs. Low priority) to prevent marketing spikes from starving 2FA codes?

### Step 2: Component Breakdown & Tech Stack
*   **API Gateway:** Request validation, auth, and entry point rate-limiting.
*   **Message Broker (e.g., Kafka / RabbitMQ):** Queue orchestration and consumer group isolation.
*   **Cache / In-Memory Store (Redis):** Idempotency key tracking, rate-limiting counters, user preference caching.
*   **Persistence Layer (PostgreSQL / MongoDB):** Notification logs, delivery statuses (`PENDING`, `SENT`, `FAILED`), template storage.
*   **Workers & Adapters:** Dedicated channel processors integrating with FCM/APNs, Twilio, SendGrid.

### Step 3: Edge Cases, Reliability & Scaling
*   **Idempotency:** How will you prevent duplicate notifications if a feature triggers the same event twice?
*   **Retry Policy & Dead Letter Queue (DLQ):** What exponential backoff strategy will you use when 3rd-party APIs (e.g., Twilio) throw transient 5xx errors?
*   **Rate Limiting & Provider Safety:** How will you cap batch promotional pushes so SendGrid/FCM don't throttle or ban FoodDash's API keys?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented Domain Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `NotificationRequest`: User ID, Template ID, Context Variables, Target Channels, Priority Level.
    *   `DeliveryResult`: Success Flag, Provider Name, Transaction/Message ID, Error Payload.
*   **Design Patterns:**
    *   **Strategy Pattern (`NotificationProvider`):** Abstract interface for concrete adapters (`SendGridEmailProvider`, `TwilioSMSProvider`, `FCMPushProvider`).
    *   **Factory Pattern (`ProviderFactory`):** Dynamic instantiation of channels.
    *   **Observer / Event Bus Pattern:** Event mapping layer to convert FoodDash domain events into notification payloads.
    *   **Decorator / Interceptor Pattern:** For rate-limiting, retries, and preference checks before worker dispatch.

---

## 4. Architectural Questions to Answer in Your Plan

Before writing code, draft your design by answering these core questions:

1. **Queue Isolation:** How will you prevent a 500,000-user promotional campaign from delaying a 2FA login code?
2. **Preference Strategy:** How will the system check user preferences and quiet hours without hitting the primary relational database on every single notification?
3. **Idempotency Strategy:** Where and how will you store idempotency keys to drop duplicate payloads safely?
4. **Failure Handling:** What happens when SendGrid returns a 429 Too Many Requests error vs. a 400 Bad Request error?