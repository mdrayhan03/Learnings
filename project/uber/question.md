# SYSTEM DESIGN BLUEPRINT 1: Global Real-Time Ride-Hailing & Driver Matching (Uber Scale)

## 1. Scenario Overview
You are the Lead Systems Architect designing the core location ingestion and matching engine for a global ride-hailing app ("MetroRide"). The engine must process continuous high-frequency location pings from active drivers and match riders with the nearest available driver in real time while maintaining sub-second latency and absolute correctness (no double allocations).

| Metric / Dimension | Requirement / Boundary |
| :--- | :--- |
| **Active Scale** | 50M active riders, 5M active drivers globally |
| **Ingestion Volatility** | 2M driver location pings/sec (every 4 seconds per driver) |
| **Latency Budget** | Matching computation < 500ms; Location tracking delay < 2s |
| **Availability & Regional SLA** | 99.999% availability with multi-region failover |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **Ingestion Layer:** How do millions of mobile driver apps maintain persistent connections for location stream ingestion without crashing edge gateways?
*   **Spatial Indexing:** How do you index moving driver coordinates dynamically in memory (e.g., Geohash vs. Uber H3 vs. QuadTree) to support fast radius queries ($O(\log N)$ or $O(1)$) without lock contention?
*   **State Machine & Match Flow:** How does the system transition a ride request through `REQUESTED` -> `SEARCHING` -> `MATCHED` -> `ACCEPTED` -> `IN_TRANSIT`?

### Step 2: Component Breakdown & Tech Stack
*   **Edge Transport:** Netty / WebSocket cluster / gRPC over HTTP/2 for bidirectional driver streaming.
*   **Stream Processing:** Apache Flink / Kafka Streams for processing spatial windows and dynamic pricing (surge calculation).
*   **Spatial Storage & Caching:** Redis Enterprise (Geospatial) / Distributed In-Memory H3 Index for hot driver locations; Cassandra / ScyllaDB for historical trip trails.
*   **Distributed Locking:** Redis Redlock / Consul for ensuring single-assignment invariants during concurrent match offers.

### Step 3: Edge Cases, Reliability & Scaling
*   **Driver Thundering Herd / Simultaneous Offers:** How to prevent 10 riders in the same geofence from picking and locking the exact same nearby driver?
*   **Network Disconnections:** How does the match orchestrator handle a driver whose connection drops right after receiving a match dispatch?
*   **Cross-Region Active-Active:** How do you handle cross-border trips or region-level data center outages without losing ongoing trip states?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented & Distributed Systems Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `LocationPing`: Driver ID, Latitude, Longitude, Heading, Speed, Timestamp.
    *   `MatchRequest`: Ride ID, Rider ID, Origin (GeoPoint), Destination (GeoPoint), Tier.
    *   `MatchOffer`: Offer ID, Ride ID, Driver ID, Expiration (Epoch ms), Status (`PENDING`, `ACCEPTED`, `REJECTED`, `EXPIRED`).
*   **Design Patterns & Constructs:**
    *   **Strategy Pattern (`SpatialIndexer`):** Abstract spatial search interface allowing runtime swap between `H3GridIndexer` and `GeohashIndexer`.
    *   **State Pattern (`RideStateMachine`):** Strict, thread-safe transactional state machine for trip lifecycle management.
    *   **Distributed Mutex / Lock Pattern:** Dynamic reservation locks on candidate drivers.

---

## 4. Architectural Questions to Answer in Your Plan

1. **Spatial Indexing & Lock Contention:** How do you continuously update driver locations in memory every 4 seconds without lock contention or thread starvation across 5 million active nodes?
2. **Double-Allocation Prevention:** What explicit locking mechanism prevents two concurrent match instances from dispatching the same driver simultaneously?
3. **Network Dropout Handling:** How does the system automatically handle a driver losing cellular connectivity during an active 15-second match offer?
4. **Data Partitioning:** What partition key topology will you use in Kafka/Redis to ensure spatial locality without creating extreme hotspot partitions in high-density downtown areas?