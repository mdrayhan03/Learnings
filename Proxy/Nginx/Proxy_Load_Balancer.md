# Comprehensive Learning Roadmap: Proxies & Load Balancing

This roadmap covers everything from core networking theory to advanced production-level configurations. Since you already know **Docker**, you can use containerization to build and test every single step locally.

---

## Phase 1: Networking Foundations (The Theory)
Before configuring tools, you must understand how data travels across the network.

### 1. The OSI Model (Focus on Layer 4 vs. Layer 7)
*   **Layer 4 (Transport):** TCP vs. UDP protocols. How routing works using only IP addresses and Port numbers (no payload inspection).
*   **Layer 7 (Application):** The HTTP/HTTPS protocol. Routing based on URLs, Headers, Cookies, and JSON bodies.
*   *Key Concept:* Understand why Layer 7 routing requires more CPU power than Layer 4 routing.

### 2. Core Network Protocols & Mechanics
*   **DNS (Domain Name System):** A-records, CNAMEs, and DNS-based round-robin load balancing.
*   **The TCP Three-Way Handshake:** SYN -> SYN-ACK -> ACK. How connections are established and maintained.
*   **TLS/SSL Handshake:** How asymmetric/symmetric encryption works, SSL certificate chains, and **SNI (Server Name Indication)**.

---

## Phase 2: Forward Proxies
A forward proxy protects, caches, and filters traffic for the **client**.



### 1. Core Concepts
*   Residential vs. Corporate proxies.
*   Anonymity levels: Transparent, Anonymous, and High Anonymity (Elite) proxies.
*   Content filtering, access control lists (ACLs), and data loss prevention (DLP).

### 2. Practical Implementation & Tools
*   **Squid Proxy:** The industry standard for open-source forward proxying.
*   *Hands-on Task:* Use Docker to spin up a Squid container. Configure your local browser to route traffic through it, and write an ACL rule to block access to specific domains (e.g., block `facebook.com`).
*   **Reverse SSH Tunneling / SOCKS5 Proxies:** Understanding alternative lightweight client proxy methods.

---

## Phase 3: Reverse Proxies & NGINX Mastery
A reverse proxy sits in front of **servers** to handle security, caching, and traffic management.



### 1. NGINX Fundamentals
*   Understanding the NGINX event-driven, non-blocking architecture (and how it differs from Apache's process-per-request model).
*   Mastering `nginx.conf` structure: `main`, `events`, `http`, `server`, and `location` blocks.

### 2. Core Reverse Proxy Features (The Must-Knows)
*   **`proxy_pass`:** Forwarding traffic from port 80/443 to internal Docker application containers.
*   **Header Manipulation:** Why and how to pass client headers forward using:
    *   `X-Forwarded-For`
    *   `X-Real-IP`
    *   `X-Forwarded-Proto`
*   **SSL/TLS Termination:** Configuring NGINX to handle SSL certificates (`ssl_certificate`, `ssl_certificate_key`) so your backend application containers can run over plain HTTP.
*   **Security Hardening:** Rate limiting requests (`limit_req_zone`), disabling server tokens, and blocking common exploit patterns.

---

## Phase 4: Load Balancers (Layer 4 & Layer 7)
Distributing high traffic across a pool of multiple backend servers.



### 1. Algorithms & Traffic Rules
*   **Static Algorithms:** Round Robin, Weighted Round Robin, IP Hash (Source IP pinning).
*   **Dynamic Algorithms:** Least Connections, Least Response Time.
*   **Sticky Sessions (Session Persistence):** How to ensure a user stays connected to the exact same server container using cookies or IP pinning.
*   **Health Checks:** Passive vs. Active health checks (How the load balancer automatically stops sending traffic to a crashed Docker container).

### 2. Tool 1: NGINX Upstream Module
*   Configuring the `upstream` block in NGINX.
*   Setting up weights, max fails, and fail timeouts.

### 3. Tool 2: HAProxy (Advanced Dedicated Balancing)
*   Why use HAProxy over NGINX? (Superior performance at scale, advanced metrics dashboard, true Layer 4 TCP proxying).
*   Understanding the HAProxy configuration file structure: `global`, `defaults`, `frontend`, and `backend`.
*   Setting up the HAProxy Stats Dashboard page.

---

> **You are here.** Everything below (Phase 5 onward) is what to learn next.
> The mental model for the rest of the journey: **API Gateways, CDNs, WAFs, and Service Meshes are all just specialized reverse proxies.** A plain reverse proxy forwards traffic; each of these adds one superpower on top (caching globally, authenticating APIs, filtering attacks, or wiring up microservices). The parent topic of this entire roadmap is **Application Delivery / Network Traffic Management** — a sub-domain of Computer Networking and System Design.

---

## Phase 5: Advanced Reverse Proxy & Caching (Filling the NGINX Gaps)
Before jumping to the cloud, master the production-grade NGINX features you skipped. **Caching especially is the bridge to understanding CDNs** — learn it here first.

### 1. Reverse Proxy Caching
*   **The Concept:** Instead of hitting your backend for every request, NGINX stores the response and serves it directly from memory/disk for the next user. This is the *exact same idea* a CDN uses, just on a single node.
*   **Key Directives:** `proxy_cache_path` (where to store), `proxy_cache` (turn it on), `proxy_cache_key` (what makes a request unique), `proxy_cache_valid` (TTL per status code).
*   **Cache Headers:** How `Cache-Control`, `Expires`, `ETag`, and `Last-Modified` from your backend control caching behavior.
*   **Cache Invalidation:** The hardest problem in computing — purging stale content, `proxy_cache_bypass`, and cache busting via versioned URLs.
*   *Hands-on Task:* Add caching to your existing NGINX reverse proxy. Use a backend that returns a timestamp; confirm the timestamp "freezes" while cached, then refreshes after the TTL expires. Watch the `X-Cache-Status: HIT/MISS` header.

    ```nginx
    # Define a cache zone (10MB of keys, max 1GB on disk, evict after 60m idle)
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

    server {
        location / {
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;   # cache successful responses for 10 min
            proxy_cache_valid 404 1m;
            add_header X-Cache-Status $upstream_cache_status;  # HIT / MISS / EXPIRED
            proxy_pass http://my_app_cluster;
        }
    }
    ```

### 2. Compression & Performance Tuning
*   **gzip / Brotli:** Compress responses at the proxy so the client downloads less. `gzip on; gzip_types text/css application/json;`
*   **Keep-Alive & Connection Pooling:** Reuse TCP connections to your upstream instead of re-handshaking every request (`keepalive` in the `upstream` block).
*   **Buffering tuning:** `proxy_buffers`, `proxy_buffer_size` — already touched on with Slowloris, now tune it intentionally.

### 3. Protocol-Aware Proxying (The Modern Web)
*   **WebSocket Proxying:** Long-lived, bidirectional connections (chat apps, live dashboards). Requires the `Upgrade` and `Connection` headers — a normal `proxy_pass` will break them.

    ```nginx
    location /ws/ {
        proxy_pass http://chat_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    ```
*   **HTTP/2 and HTTP/3 (QUIC):** Multiplexing many requests over one connection; QUIC runs over UDP. Learn how `listen 443 ssl http2;` changes things and why HTTP/3 matters for mobile.
*   **mTLS (Mutual TLS):** Not just the server proving its identity — the *client* also presents a certificate. Used for service-to-service trust and zero-trust networks (`ssl_verify_client on;`).

### 4. Sticky Sessions Done Right
*   You listed this in Phase 4 — now actually implement it. NGINX `ip_hash`, or cookie-based stickiness (`sticky cookie` in NGINX Plus / open-source alternatives), and *why* the modern answer is usually "make your app stateless and store sessions in Redis instead."

---

## Phase 6: CDN & Edge Caching
A **CDN is a globally distributed caching reverse proxy.** Same caching skill from Phase 5, but the proxy nodes live in hundreds of cities worldwide so users hit the nearest edge.

### 1. Core Concepts
*   **Edge nodes / PoPs (Points of Presence):** A user in Tokyo hits the Tokyo edge, not your origin in Virginia.
*   **Origin Shielding:** A single mid-tier cache that protects your origin from the "thundering herd" of all edge nodes asking at once.
*   **Cache Hit Ratio:** The single most important CDN metric — what % of requests never reach your origin.
*   **Static vs. Dynamic content:** Why images/CSS/JS cache trivially, and how to cache (or deliberately not cache) API responses and HTML.
*   **Anycast Routing:** How one IP address can route to the geographically nearest server automatically (ties back to your DNS knowledge).

### 2. Practical Implementation
*   **Cloudflare (free tier):** Put a real domain behind Cloudflare, set caching rules, and watch the analytics dashboard show cache hits vs. origin pulls. This is the fastest way to make Phase 5 caching "click."
*   *Hands-on Task:* Configure cache rules so static assets cache at the edge for 1 year while `/api/*` bypasses the cache entirely. Use `curl -I` and inspect the `CF-Cache-Status` header.
*   Other tools to be aware of: **AWS CloudFront**, **Fastly** (programmable edge via VCL), **Akamai**.

---

## Phase 7: API Gateways (Reverse Proxy for Microservices)
An **API Gateway is a reverse proxy with extra brains.** When you have dozens of microservices, you don't want each one handling auth, rate limiting, and routing separately — the gateway centralizes it at the front door.

### 1. Core Responsibilities (What a Gateway Adds Over Plain `proxy_pass`)
*   **Authentication & Authorization:** API keys, JWT validation, OAuth2 / OpenID Connect — centralized so backends never see an unauthenticated request.
*   **Per-Consumer Rate Limiting & Quotas:** Limit *per API key / per customer*, not just per IP.
*   **Request/Response Transformation:** Rewrite headers, strip fields, convert formats before the request reaches the service.
*   **Routing & Versioning:** `/api/v1/*` → service A, `/api/v2/*` → service B. Canary releases and blue-green deploys.
*   **Request Aggregation:** One client call fans out to several microservices and the gateway stitches the responses together.

### 2. Tools & Hands-On
*   **Kong** (built on NGINX/OpenResty — directly extends what you already know), **KrakenD** (stateless, config-driven, great for aggregation), **Envoy** (the modern CNCF proxy, also the engine inside service meshes).
*   *Hands-on Task:* Run **Kong** in Docker in front of 2 backend services. Add a key-auth plugin and a rate-limiting plugin. Confirm that a request without a valid API key is rejected by the gateway *before* it ever reaches a backend.

---

## Phase 8: Service Mesh (Internal Proxy-per-Service)
So far every proxy sat at the *edge* (north-south traffic). A **service mesh** handles traffic *between* your internal microservices (east-west traffic) by attaching a tiny proxy to every single service.

### 1. Core Concepts
*   **The Sidecar Pattern:** Every microservice pod gets its own proxy container (usually **Envoy**) that intercepts all its inbound/outbound traffic. The app doesn't even know it's there.
*   **Data Plane vs. Control Plane:** The sidecars (data plane) do the work; a central brain (control plane) configures them all.
*   **What you get "for free":** Automatic mTLS between every service, retries, timeouts, circuit breaking, fine-grained traffic splitting (5% to v2), and distributed tracing — *without changing application code*.

### 2. Tools & Hands-On
*   **Linkerd** (simpler, start here) vs. **Istio** (powerful, complex, Envoy-based).
*   *Hands-on Task (needs Kubernetes — use `kind`, `minikube`, or k3d in Docker):* Deploy a 2-service demo app, install Linkerd, and inject the mesh. Observe automatic mTLS and the live traffic topology graph. This is your introduction to Kubernetes networking too.

---

## Phase 9: Cloud Load Balancers & Edge Security
How everything you built locally maps onto managed cloud services you'd use in a real job.

### 1. Managed Cloud Load Balancers
*   **AWS:** Application Load Balancer (**ALB** = your Layer 7 NGINX, managed), Network Load Balancer (**NLB** = your Layer 4 HAProxy, managed, ultra-high throughput), and the legacy Classic LB. Learn target groups, listeners, and health checks — they map 1:1 to concepts you already know.
*   **GCP / Azure equivalents:** Cloud Load Balancing, Azure Application Gateway / Front Door.
*   **Autoscaling:** How cloud LBs add/remove backend instances automatically based on load (the dynamic version of your static `upstream` list).

### 2. Edge Security (WAF & DDoS)
*   **Web Application Firewall (WAF):** You touched ModSecurity in Phase 3 — now learn managed WAFs (AWS WAF, Cloudflare WAF) and the **OWASP Top 10** attacks they defend against (SQL injection, XSS, CSRF).
*   **DDoS Protection:** Volumetric (L3/4) vs. application-layer (L7) attacks, and how Anycast networks absorb them.
*   **Bot Management & Geo-blocking:** Rate-limiting by reputation, country, and behavior.

---

## Phase 10: Observability & Operations
The skill that separates a toy setup from a production system: knowing what your proxy is actually doing.

*   **Access & Error Logs:** Custom NGINX `log_format` (capture upstream response time, cache status, request ID).
*   **Metrics:** Expose NGINX/HAProxy metrics and scrape them with **Prometheus**; visualize in **Grafana** (requests/sec, p95 latency, error rate, upstream health).
*   **Distributed Tracing:** Propagate a trace ID (`X-Request-ID`) from the edge proxy through every microservice (Jaeger / OpenTelemetry) so you can follow one request across the whole system.
*   **Zero-Downtime Operations:** Graceful reloads (`nginx -s reload`), connection draining when removing a backend, and blue-green / canary deployments at the proxy layer.

---

## Phase 11: Practical Capstone Projects (To Build with Docker)

Solidify everything by building these architectures locally. Do them in order — each adds a layer.

### Project 1: The Secure Web Shell (Phases 3–5)
1. Create a Docker network. Spin up 2 web app containers on plain HTTP with **no exposed ports**.
2. Spin up an NGINX container exposing `80` and `443`. Generate self-signed SSL certs with OpenSSL and terminate SSL at NGINX.
3. Route by URL path (`/api/v1` → App 1, `/static` → App 2) and **add response caching** to the static path. Verify with the `X-Cache-Status` header.

### Project 2: High Availability Cluster with HAProxy (Phase 4)
1. Spin up 3 identical web app containers behind an HAProxy container (Round Robin, active health checks).
2. Hit it repeatedly and watch traffic distribute across all 3.
3. `docker stop` one container and confirm HAProxy reroutes seamlessly with zero dropped requests. Open the HAProxy stats dashboard to watch it happen live.

### Project 3: Rate Limiting & The Security Wall (Phases 3 & 9)
1. Configure NGINX to cap a single IP at 5 req/s with a burst buffer.
2. Hammer it with `ApacheBench` (`ab`) or `wrk` and watch excess requests rejected with `429 Too Many Requests`.

### Project 4: The Microservices Front Door (Phase 7) — *Capstone*
1. Run 3 small microservices (users, orders, products) in Docker, each with no public ports.
2. Put **Kong** in front as the single API gateway. Add key-auth + per-consumer rate limiting + path-based routing.
3. Confirm: unauthenticated requests die at the gateway, and each `/users`, `/orders`, `/products` path routes to the correct service. This single project ties Phases 3, 4, 5, and 7 together.

### Project 5 (Stretch): Service Mesh on Kubernetes (Phase 8)
1. Spin up a local cluster with `kind` or `k3d`.
2. Deploy a 2-service demo app, install **Linkerd**, and inject the mesh.
3. Observe automatic mTLS, the live traffic graph, and a 90/10 traffic split between v1 and v2 of a service.