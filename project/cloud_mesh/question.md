# SYSTEM DESIGN BLUEPRINT 5: Multi-Region Distributed Peer-to-Peer Storage & Sync Engine (CloudMesh Scale)

## 1. Scenario Overview
You are tasked with designing the control plane, metadata registry, and synchronization layer for a hybrid enterprise file storage mesh network ("CloudMesh"). The system allows users to store petabyte-scale files divided into encrypted chunks distributed across localized LAN edge nodes and multi-region cloud object stores, keeping file systems synced across millions of global user endpoints.

| Metric / Dimension | Requirement / Boundary |
| :--- | :--- |
| **Catalog Scale** | 50 million active endpoints; 100 PB total catalog size |
| **Sync SLA** | Metadata file delta propagation < 500ms globally |
| **Deduplication Target** | Global content-addressable block deduplication ($>30\%$ storage savings) |
| **Fault Tolerance** | System must survive complete loss of an entire cloud region without data corruption |

---

## 2. PHASE 1: High-Level Design (HLD) Plan

### Step 1: System Architecture & Data Flow
*   **File Partitioning & Chunking:** How do local client agents divide large files into variable-sized chunks using Content-Defined Chunking (e.g., Rabin Fingerprinting / FastCDC) to optimize deduplication?
*   **Metadata Orchestration:** How does the metadata ledger track file trees, directory structures, block maps, and permissions globally without causing distributed lock deadlocks?
*   **Peer Discovery & Traversal:** How do endpoints locate neighboring LAN peers holding requested file chunks to avoid expensive WAN bandwidth usage, using NAT traversal (STUN/TURN/ICE)?

### Step 2: Component Breakdown & Tech Stack
*   **Control Plane Gateway:** gRPC services backed by Envoy Proxy for bidirectional desktop/mobile client streaming.
*   **Distributed Metadata Store:** CockroachDB / Spanner for transactional metadata consistency, combined with a Distributed Hash Table (DHT / Kademlia protocol) for peer location tracking.
*   **Block Repository:** AWS S3 / Google Cloud Storage for remote cold block storage; local client disk caches for P2P chunk sharing.
*   **Sync Bus:** Apache Kafka / NATS JetStream for broadcasting folder modification deltas.

### Step 3: Edge Cases, Reliability & Scaling
*   **Concurrent Write Conflicts:** How do you resolve situations where two users modify the exact same file offline simultaneously and reconnect at the same time (e.g., Conflict-Free Replicated Data Types vs. Vector Clocks vs. Conflict Files)?
*   **Network Partition & Partial Block Uploads:** How does the system handle an upload failing midway through a 50GB transfer, leaving incomplete chunk sets across nodes?
*   **Bandwidth & Resource Throttling:** How do you calculate optimal peer block download maps so local network links aren't saturated?

---

## 3. PHASE 2: Low-Level Design (LLD) Blueprint

### Object-Oriented & Distributed Systems Architecture
*   **Data Models (`dataclasses` / Pydantic):**
    *   `FileNode`: Node ID, Path, Type (`FILE`/`DIRECTORY`), Hash, Version Vector, Parent ID.
    *   `ChunkManifest`: Chunk Hash (SHA-256), Size, Storage Locations (List of Peer Nodes / Object Store Keys).
    *   `SyncDelta`: Client ID, Sequence No, Target File Path, Operations List (`ADD_BLOCK`, `DELETE_BLOCK`, `UPDATE_METADATA`).
*   **Design Patterns & Constructs:**
    *   **Merkle Tree Pattern:** Quick comparison of directory structures between endpoints to isolate modified files in $O(\log N)$ time.
    *   **Strategy Pattern (`NATTraversalStrategy`):** Dynamic switching between Direct TCP, STUN/UPnP Local Discovery, and TURN Relay fallback.
    *   **Observer Pattern:** Multi-client directory watching engine capturing localized file system modification events.

---

## 4. Architectural Questions to Answer in Your Plan

1. **Content-Defined Chunking Mechanics:** Explain why fixed-size chunking fails for file synchronization engines when a user inserts a single byte at the beginning of a file, and how dynamic chunking (FastCDC) resolves this.
2. **Distributed Conflict Resolution:** Write down the explicit state transition or Vector Clock / CRDT algorithm you will deploy to handle simultaneous offline edits to the same document tree.
3. **Merkle Tree State Verification:** How are Merkle trees constructed and exchanged between the client and cloud to verify missing chunks across a 100,000-file directory in seconds?
4. **P2P NAT Traversal Protocol:** How will your tracker service orchestrate peer-to-peer data transfers between two clients trapped behind strict corporate symmetric NAT firewalls?