# 🌐 High-Level Design (HLD) Enterprise Question Bank

These challenges evaluate your capacity to balance trade-offs across microservice boundaries, data storage lifecycles, caching tiers, and messaging topologies under immense real-world strain.

---

### Challenge 1: The Global Real-Time Ride-Hailing Coordination Fabric (Uber Scale)
* **The Core Requirements:** Architect a real-time matching engine connecting millions of active riders and drivers globally. The platform must handle continuous high-frequency location ping updates (every 4 seconds) from drivers and resolve proximity queries matching riders instantly.
* **Scale & Volatility Metrics:** 50 million active users daily, 5 million active drivers, peak ingestion spikes of 2 million concurrent driver location pings per second, and sub-second matching thresholds.
* **Deep Architectural Concerns:**
  * Define an ingestion and spatial partitioning topology (e.g., Dynamic Geo-sharding vs. Static Grid Indexing like H3/S2) that updates spatial locations in memory without causing database thrashing.
  * Structure the distributed matching state flow to guarantee that a driver is never dual-assigned or starved of requests across edge instances.
  * Design a cross-region active-active failover strategy ensuring that if a major data center completely drops connection, ongoing active trips do not lose their state trackers.

### Challenge 2: The High-Throughput IoT Video Analytics Ingestion Fabric (Cam-Cloud Scale)
* **The Core Requirements:** Design the ingestion and stream-processing infrastructure for an enterprise smart-surveillance engine. The platform connects millions of continuous stream IP cameras to analyze motion, face matches, and security breaches, archiving raw video blocks while routing alerts to localized client frames.
* **Scale & Volatility Metrics:** 10 million deployed camera streams, 1 Gbps global ingress bandwidth ceiling per ingestion edge, and live streaming video block metadata evaluation under a hard <200ms processing delay envelope.
* **Deep Architectural Concerns:**
  * Map out the ingestion boundary layer (Load balancers, API gateways supporting WebSockets/RTSP protocols) and how you isolate media parsing from downstream compute clusters.
  * Design the data streaming tier (e.g., Kafka vs. Pulsar vs. Kinesis) to handle partition keys ensuring sequential block evaluation for individual cameras without causing Head-of-Line (HoL) blocking across the cluster.
  * Create a tiered-storage lifecycle pattern that stores raw video segments in a low-latency cache for 24 hours, moves them to object stores for 30 days, and moves cold files to glacier tape archiving without breaking search indexing queries.

### Challenge 3: The Low-Latency Globally Distributed Ad-Click Tracking Dashboard
* **The Core Requirements:** Design a global click-tracking and analytics aggregation layout for a massive search engine. The network must capture billions of search, click, and interaction events per hour and render up-to-the-minute campaign analytics back to corporate marketing entities instantly.
* **Scale & Volatility Metrics:** 150,000 ingest impressions per second, 10 billion tracking data events daily, and analytics dashboard reads must resolve in under 500 milliseconds across global time bounds.
* **Deep Architectural Concerns:**
  * Evaluate the trade-offs between Lambda vs. Kappa stream-processing architectures to maintain accurate financial billing computations alongside real-time analytical estimation.
  * Define your analytical storage pattern (e.g., ClickHouse, Druid, or Cassandra-based wide-column families) to support heavy write rates alongside fast slicing/dicing queries.
  * Address **Hotspot Mitigation**: How does your database partition topology prevent a sudden, viral marketing campaign from overwhelming a single database node?

### Challenge 4: The Flash-Sale E-Commerce Inventory & Order Ledger (Amazon Scale)
* **The Core Requirements:** Design the absolute core ordering pipeline for a global retail system experiencing a viral holiday flash sale. The infrastructure must coordinate checkout states, coupon validations, payment gateway pipelines, and real-time absolute item inventory countdown blocks.
* **Scale & Volatility Metrics:** 100 million browse users, a flash inventory payload of 10,000 limited-edition units, and transaction spikes exceeding 100,000 checkout attempts per second targeting the exact same inventory pool.
* **Deep Architectural Concerns:**
  * Architect a robust caching and distributed locking framework (e.g., Redis Lua scripting, token buckets, or pessimistic database row reservations) to prevent overselling inventory.
  * Detail how you decouple the ordering state pipeline from payment gateways using the Saga Pattern or Two-Phase Commit to ensure data consistency without starving application worker thread pools during network timeouts.
  * Implement an isolated circuit-breaker layout to ensure that if the downstream shipping or email confirmation services crash, the core checkout processing funnel remains open.

### Challenge 5: The Peer-to-Peer Multi-Region LAN/WAN Hybrid Media Sync Mesh
* **The Core Requirements:** Design a massively scalable content delivery mesh networks tracking local files. Peers within localized corporate networks (LANs) and outer WAN clouds must discover each other, announce chunk ownership, and stream huge media file fragments efficiently without relying on centralized bandwidth pipes.
* **Scale & Volatility Metrics:** 50 million active peer terminal clients globally, 100PB of shared files, and tracker metadata queries resolving across fluctuating node membership boundaries.
* **Deep Architectural Concerns:**
  * Design a distributed discovery tier (e.g., Distributed Hash Tables (DHT) like Kademlia vs. centralized coordinated Tracker microservices clusters) to track file chunk layouts.
  * Address network topology traversal (NAT Traversal, STUN, TURN, ICE protocols) to manage peer configurations that are trapped behind strict corporate firewalls.
  * Implement bandwidth and mesh fairness mechanics: How do you coordinate the peer selection engine to prioritize local high-speed LAN links over slow, costly internet links?

---
---
---
## ⚡ How to Attack Your First System Diagram
To get the most out of these HLD questions, don't just list technologies. Pick one challenge and break it down by writing out:

1. System Interface APIs: The core endpoints or event payloads required to run the operation.

2. Data Model Choices: The precise storage choices (e.g., when to use a relational database vs. a key-value store, vs. a column-family store) and your data partitioning strategy.

3. Core Component Diagram Blueprint: A step-by-step description of how data moves from the client, through load balancers, messaging queues, cache rings, and workers down to cold database storage pools.