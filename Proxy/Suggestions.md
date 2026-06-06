# Proxy & Load Balancing — Learning Checklist

Track your progress phase by phase. Update the **Status** column to `Done` as you finish each goal.
Status legend: `Done` · `In Progress` · `Pending`

> Phases 1–4 are marked **Done** (already studied). Start from Phase 5.

---

## Phase 1: Networking Foundations

| #   | Goal (Sub-phase)                                              | Status |
| --- | ------------------------------------------------------------ | ------ |
| 1.1 | OSI Model — Layer 4 (TCP/UDP, IP+Port routing)               | Done   |
| 1.2 | OSI Model — Layer 7 (HTTP routing by URL/header/cookie)      | Done   |
| 1.3 | DNS — A-records, CNAMEs, DNS round-robin                     | Done   |
| 1.4 | TCP Three-Way Handshake (SYN → SYN-ACK → ACK)                | Done   |
| 1.5 | TLS/SSL Handshake + SNI                                      | Done   |

---

## Phase 2: Forward Proxies

| #   | Goal (Sub-phase)                                             | Status |
| --- | ----------------------------------------------------------- | ------ |
| 2.1 | Anonymity levels (Transparent / Anonymous / Elite)          | Done   |
| 2.2 | Content filtering, ACLs, DLP                                | Done   |
| 2.3 | Squid Proxy in Docker + ACL domain blocking                 | Done   |
| 2.4 | SOCKS5 / Reverse SSH tunneling basics                       | Done   |

---

## Phase 3: Reverse Proxies & NGINX

| #   | Goal (Sub-phase)                                            | Status |
| --- | ---------------------------------------------------------- | ------ |
| 3.1 | NGINX event-driven architecture vs Apache                  | Done   |
| 3.2 | `nginx.conf` structure (main/events/http/server/location)  | Done   |
| 3.3 | `proxy_pass` forwarding                                    | Done   |
| 3.4 | Header manipulation (X-Forwarded-For, X-Real-IP, Proto)    | Done   |
| 3.5 | SSL/TLS Termination                                        | Done   |
| 3.6 | Security hardening (rate limiting, server tokens, WAF)     | Done   |

---

## Phase 4: Load Balancers

| #   | Goal (Sub-phase)                                           | Status |
| --- | --------------------------------------------------------- | ------ |
| 4.1 | Static algorithms (Round Robin, Weighted, IP Hash)        | Done   |
| 4.2 | Dynamic algorithms (Least Connections, Least Response)    | Done   |
| 4.3 | Health checks (active vs passive)                         | Done   |
| 4.4 | NGINX `upstream` module (weights, max_fails, timeouts)    | Done   |
| 4.5 | HAProxy (frontend/backend, stats dashboard)               | Done   |

---

## Phase 5: Advanced Reverse Proxy & Caching

| #   | Goal (Sub-phase)                                                | Status  |
| --- | --------------------------------------------------------------- | ------- |
| 5.1 | Reverse proxy caching (`proxy_cache`, cache zones, TTLs)        | Pending |
| 5.2 | Cache headers (Cache-Control, ETag, Last-Modified)              | Pending |
| 5.3 | Cache invalidation & busting (`proxy_cache_bypass`)             | Pending |
| 5.4 | Hands-on: add caching + verify `X-Cache-Status` HIT/MISS        | Pending |
| 5.5 | Compression (gzip / Brotli)                                     | Pending |
| 5.6 | Keep-alive & upstream connection pooling                        | Pending |
| 5.7 | Buffer tuning (`proxy_buffers`, `proxy_buffer_size`)            | Pending |
| 5.8 | WebSocket proxying (Upgrade/Connection headers)                 | Pending |
| 5.9 | HTTP/2 and HTTP/3 (QUIC) proxying                               | Pending |
| 5.10| mTLS (mutual TLS, `ssl_verify_client`)                         | Pending |
| 5.11| Sticky sessions (ip_hash / cookie / Redis-backed stateless)    | Pending |

---

## Phase 6: CDN & Edge Caching

| #   | Goal (Sub-phase)                                               | Status  |
| --- | -------------------------------------------------------------- | ------- |
| 6.1 | Edge nodes / PoPs concept                                      | Pending |
| 6.2 | Origin shielding & thundering herd                             | Pending |
| 6.3 | Cache hit ratio metric                                         | Pending |
| 6.4 | Static vs dynamic content caching                              | Pending |
| 6.5 | Anycast routing                                                | Pending |
| 6.6 | Hands-on: domain behind Cloudflare + cache rules               | Pending |
| 6.7 | Inspect `CF-Cache-Status` header                               | Pending |

---

## Phase 7: API Gateways

| #   | Goal (Sub-phase)                                               | Status  |
| --- | -------------------------------------------------------------- | ------- |
| 7.1 | Authentication & authorization (API keys, JWT, OAuth2/OIDC)    | Pending |
| 7.2 | Per-consumer rate limiting & quotas                            | Pending |
| 7.3 | Request/response transformation                                | Pending |
| 7.4 | Routing & versioning (canary, blue-green)                      | Pending |
| 7.5 | Request aggregation                                            | Pending |
| 7.6 | Tools overview: Kong / KrakenD / Envoy                         | Pending |
| 7.7 | Hands-on: Kong in Docker + key-auth + rate-limit plugins       | Pending |

---

## Phase 8: Service Mesh

| #   | Goal (Sub-phase)                                               | Status  |
| --- | -------------------------------------------------------------- | ------- |
| 8.1 | Sidecar pattern (Envoy per service)                            | Pending |
| 8.2 | Data plane vs control plane                                    | Pending |
| 8.3 | Auto-mTLS, retries, timeouts, circuit breaking                 | Pending |
| 8.4 | Traffic splitting & distributed tracing                        | Pending |
| 8.5 | Linkerd vs Istio overview                                       | Pending |
| 8.6 | Hands-on: deploy app + Linkerd on kind/k3d                     | Pending |

---

## Phase 9: Cloud Load Balancers & Edge Security

| #   | Goal (Sub-phase)                                               | Status  |
| --- | -------------------------------------------------------------- | ------- |
| 9.1 | AWS ALB (L7) vs NLB (L4) vs Classic                            | Pending |
| 9.2 | Target groups, listeners, cloud health checks                  | Pending |
| 9.3 | GCP / Azure LB equivalents                                     | Pending |
| 9.4 | Autoscaling with cloud LBs                                      | Pending |
| 9.5 | Managed WAF + OWASP Top 10                                      | Pending |
| 9.6 | DDoS protection (L3/4 vs L7)                                    | Pending |
| 9.7 | Bot management & geo-blocking                                   | Pending |

---

## Phase 10: Observability & Operations

| #    | Goal (Sub-phase)                                              | Status  |
| ---- | ------------------------------------------------------------ | ------- |
| 10.1 | Custom NGINX log_format (upstream time, cache status)        | Pending |
| 10.2 | Metrics with Prometheus                                      | Pending |
| 10.3 | Dashboards with Grafana                                      | Pending |
| 10.4 | Distributed tracing (X-Request-ID, Jaeger/OpenTelemetry)    | Pending |
| 10.5 | Zero-downtime ops (graceful reload, draining, canary)       | Pending |

---

## Phase 11: Capstone Projects (Docker)

| #    | Goal (Project)                                               | Status  |
| ---- | ----------------------------------------------------------- | ------- |
| 11.1 | Project 1 — Secure Web Shell (SSL term + path routing + cache) | Pending |
| 11.2 | Project 2 — HA Cluster with HAProxy (RR + health + failover)   | Pending |
| 11.3 | Project 3 — Rate Limiting & Security Wall (ab/wrk test)        | Pending |
| 11.4 | Project 4 — Microservices Front Door with Kong (capstone)      | Pending |
| 11.5 | Project 5 — Service Mesh on Kubernetes with Linkerd (stretch)  | Pending |
