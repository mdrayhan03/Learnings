# SYSTEM DESIGN BLUEPRINT 3: Global IoT Video Streaming Ingestion & Edge Analytics Fabric (CamCloud Scale)

## 1. Scenario Overview
You are tasked with designing the global streaming ingestion and real-time computer vision processing pipeline for a smart surveillance platform ("CamCloud"). Millions of IP security cameras stream continuous encrypted video segments to cloud edge nodes, which analyze frame streams for motion/faces in under 200ms and archive raw media to cost-effective tiered storage.

| Metric / Dimension | Requirement / Boundary |
| :--- | :--- |
| **Connected Devices** | 10 million continuous video stream endpoints |
| **Global Ingress Bandwidth** | ~10 Terabits per second (Tbps) global edge ingress |
| **Detection SLA** | Motion / Security breach event alert dispatch < 200ms |
| **Storage Lifecycle** | 24-hr Hot Storage (In-memory/SSD) -> 30-day Warm (S3 Standard) -> 7-year Cold (Glacier) |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **Protocol & Connection Management:** How do edge gateways maintain persistent, low-overhead WebRTC/RTSP/RTMP ingress streams from constrained embedded IoT devices across fluctuating internet topologies?
*   **Stream Decoupling:** How is raw binary media stream payload split into analytical metadata frames and video chunk segments without causing Head-of-Line (HoL) blocking?
*   **Alert Pipeline:** How are real-time threat metadata events routed instantly from AI inference nodes to mobile push engines?

### Step 2: Component Breakdown & Tech Stack
*   **Ingestion Edge Gateway:** Kinesis Video Streams / Custom Netty RTSP Gateway running on Kubernetes edge clusters.
*   **Stream Buffering:** Apache Pulsar / Kafka with tiered storage enabled (using native segment offloading).
*   **Compute Inference Cluster:** GPUs/T4 worker clusters running lightweight ONNX / TensorRT models for real-time frame classification.
*   **Storage Hierarchy:** MinIO / AWS S3 + AWS S3 Glacier Flexible Retrieval with automated S3 Lifecycle Rules and metadata indexing in ClickHouse.

### Step 3: Edge Cases, Reliability & Scaling
*   **Network Jitter & Packet Loss:** How does the ingestion gateway handle variable bitrate (VBR) spikes or regional internet fiber disruptions without dropping frames?
*   **Edge Compute Partitioning:** How do you dynamically route streaming traffic to compute nodes so that frame inference workload is balanced across GPU worker pools?
*   **Cost & Storage Optimization:** How do you index billions of 5-second video chunks so users can perform instant timestamp-based playback queries without exploding index storage costs?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented & Distributed Systems Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `StreamSegmentHeader`: Camera ID, Segment Sequence ID, Timestamp, Duration, Encoding, Resolution.
    *   `DetectionEvent`: Event ID, Camera ID, Event Type (`MOTION`, `FACE_MATCH`), Confidence Score, Bounding Box, Frame Hash.
    *   `StorageManifest`: Camera ID, Segment ID, Hot Path URI, Cold Archive Key, Expiration Epoch.
*   **Design Patterns & Constructs:**
    *   **Pipe and Filter Architecture:** Sequentially processing raw byte streams through Decryption, Frame Extraction, Inference, and Archival filters.
    *   **Adapter Pattern (`StorageAdapter`):** Standardized media storage operations across local SSDs, S3 Object Store, and Glacier Archival APIs.
    *   **Flyweight Pattern:** Efficiently allocating and reusing heavy video frame memory buffers in worker processes.

---

## 4. Architectural Questions to Answer in Your Plan

1. **Backpressure Strategy:** When downstream ML inference worker clusters experience temporary processing backpressure, how does your ingestion pipeline degrade gracefully without dropping raw video archives?
2. **Indexing Metadata at Scale:** How will you schema design your database (e.g., ClickHouse or Cassandra) to handle 10 billion daily segment inserts while supporting sub-second spatial-temporal video clip lookup queries?
3. **Edge-to-Cloud Routing:** What geo-DNS / Anycast routing topology will you deploy to bind camera devices to the closest edge ingress proxy with minimum latency?
4. **Data Security & Privacy:** How do you enforce end-to-end encryption (E2EE) for stored video chunks while allowing cloud-based AI compute nodes to inspect individual frame buffers safely?