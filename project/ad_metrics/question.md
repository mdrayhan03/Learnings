# SYSTEM DESIGN BLUEPRINT 4: Low-Latency Global Ad-Click Aggregator & Analytics Engine (AdMetrics Scale)

## 1. Scenario Overview
You are designing the click-tracking, fraud-detection, and real-time billing aggregation system for a global ad-tech platform ("AdMetrics"). The service receives billions of ad interaction events daily from web browsers and mobile apps worldwide, processes raw streams to detect invalid click activity (fraud/bots), updates advertiser budget balances, and feeds real-time campaign performance dashboards.

| Metric / Dimension | Requirement / Boundary |
| :--- | :--- |
| **Ingestion Volume** | 150,000 ad events/sec (10+ billion events daily) |
| **Dashboard Query Latency** | Sub-500ms aggregation query response across global ad accounts |
| **Billing Correctness** | Exactly-once event processing semantics for financial billing |
| **Fraud Detection Envelope** | Fraudulent click filtration < 2 seconds post-click |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **Ingestion Edge:** How do click redirect endpoints log engagement events with sub-10ms latency to preserve seamless end-user browser redirects?
*   **Processing Framework:** How do you execute real-time stream aggregation (using Lambda vs. Kappa architecture) to maintain both instant dashboard visibility and auditably accurate billing reconciliation?
*   **Hotspot Management:** How do you prevent viral ad campaigns (millions of clicks per minute on a single ad ID) from causing partition hotspots in stream brokers and analytical databases?

### Step 2: Component Breakdown & Tech Stack
*   **Ingestion Gateways:** Go / Rust lightweight HTTP microservices behind AWS ALB with Anycast routing.
*   **Stream Engine:** Apache Flink running tumbling and sliding window joins against ad metadata streams.
*   **Real-time Analytics Store:** ClickHouse / Apache Druid for columnar OLAP time-series aggregation.
*   **Cold Storage & Audit:** Apache Iceberg / Parquet files on S3 processed via Apache Spark for nightly reconciliation.

### Step 3: Edge Cases, Reliability & Scaling
*   **Duplicate Event Removal:** How do you handle client-side double-clicks, network retry dupes, and automated web scraper spam without double-charging advertisers?
*   **Late-Arriving Data:** How do streaming tumbling windows process delayed click events (e.g., mobile devices coming back online after flying in airplane mode) without distorting closed financial reporting windows?
*   **Budget Depletion Race:** How do you stop serving ads within seconds when an advertiser's daily balance reaches zero to avoid over-delivery financial loss?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented & Distributed Systems Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `RawClickEvent`: Impression ID, Ad ID, Advertiser ID, User IP Hash, User Agent, Timestamp, Redirect URL.
    *   `EnrichedClickEvent`: Click ID, Fraud Score, Is Valid (Bool), Geolocation, Billing Amount.
    *   `AggregatedAdMetrics`: Campaign ID, Time Window, Total Clicks, Valid Clicks, Total Spend.
*   **Design Patterns & Constructs:**
    *   **Decorator / Interceptor Pattern:** Chain of fraud checkers (IP Blacklist Checker, Frequency Rate Limit Checker, ML Anomaly Checker).
    *   **Sliding Window Aggregator:** Stateful stream processing pattern calculating moving metrics over time windows.
    *   **Two-Phase Commit / Exactly-Once Sink:** Transactional Kafka-to-ClickHouse sink connector preventing duplicated counts.

---

## 4. Architectural Questions to Answer in Your Plan

1. **Exactly-Once Delivery Semantics:** How will you construct your stream processing pipeline (from HTTP collection to database aggregation) to guarantee **exactly-once** processing for advertiser billing?
2. **Late-Data Windowing:** Explain how you will use Apache Flink **Watermarks** and **Allowed Lateness** strategies to deal with events arriving 2 hours after occurrence.
3. **Columnar Database Index Strategy:** How will you structure primary keys and sorting keys in ClickHouse/Druid to serve high-throughput campaign aggregate dashboards instantly without high disk IOPS?
4. **Budget Circuit Breaker:** How does the system propagate a "budget exhausted" status back to edge ad-serving servers globally within < 1 second to halt active ad auctions?