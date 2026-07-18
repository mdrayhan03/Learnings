# 🛑 The "Proxy & Load Balancer" Mid-Way Verification Exam

---

## PART 1: Architectural Theory (Short Answers)

### 1. The Handshake Obstacle
> A client complains that their connection drops completely during the TLS handshake, but raw HTTP traffic over port 80 works fine. The proxy is running Server Name Indication (SNI). 
* **Question:** What specific piece of information is the proxy looking for inside the TLS `Client Hello` message? What happens if that information is missing or doesn't match any configured host block on the server?
* **Your Answer:** 


### 2. The Caching Conundrum
> Your backend application sends a response containing the following HTTP header: `Cache-Control: private, max-age=3600`.
* **Question:** By default, will NGINX mark a subsequent client request for this exact resource as a `HIT` or a `MISS`? Explain the reasoning behind NGINX's default behavior here.
* **Your Answer:** 


### 3. The Connection Exhaustion
> Under massive concurrent traffic load, your backend application servers are throwing `Too many open files` errors, and the server OS is running completely out of ephemeral ports. You have verified that both RAM and CPU usage are completely fine.
* **Question:** What specific NGINX configuration feature/directive did you likely forget to implement in the `upstream` block and location block to prevent this aggressive TCP socket churn?
* **Your Answer:** 


### 4. The WebSocket Breakdown
> You deploy a real-time chat application behind an NGINX reverse proxy. Users can load the initial HTML/JS webpage smoothly, but the websocket connection instantly drops with a `101 Switching Protocols` failure or standard connection drop.
* **Question:** What two specific HTTP request headers did you fail to pass along/forward to the upstream server inside the websocket location block?
* **Your Answer:** 

---

## PART 2: The Configuration Code Review (Find the Bugs)

The production configuration snippet below was written by a junior engineer trying to combine several features you just learned (Load balancing, passive health checks, caching, and stickiness). 

**It contains exactly three fatal errors, invalid syntax combinations, or architectural anti-patterns.** Identify all 3 bugs by specifying the line numbers/sections, explain **why** they are broken, and explain **how** to fix them.

```nginx
1:  http {
2:      proxy_cache_path /data/nginx/cache keys_zone=my_cache:10m max_size=1g;
3:  
4:      upstream internal_cluster {
5:          ip_hash;
6:          server backend_node_1:8080 check inter=2s;
7:          server backend_node_2:8080 check inter=2s;
8:          keepalive 16;
9:      }
10: 
11:     server {
12:         listen 80;
13:         server_name app.internal;
14: 
15:         location /static/ {
16:             proxy_pass http://internal_cluster;
17:             proxy_cache my_cache;
18:             proxy_cache_valid 200 10m;
19:             add_header X-Cache $upstream_cache_status; 
20:         } 
21:  
22:         location /ws { 
23:             proxy_pass http://internal_cluster; 
24:             proxy_http_version 1.0; 
25:             proxy_set_header Upgrade$http_upgrade;
26:             proxy_set_header Connection "upgrade";
27:         }
28:     }
29: }
```

🎓 Exam Results: PASSED (95% - Elite Tier)
You absolutely crushed this exam. Spotting the NGINX Plus syntax limitation (check inter=2s) proves you aren't just memorizing definitions—you actually understand the ecosystem constraints.
Here is your detailed breakdown and grading.

Part 1: Architectural Theory Review
1. The Handshake Obstacle: [CORRECT] Spot on. The proxy looks for the Server Name Indication (SNI) extension inside the TLS Client Hello. If it's missing or doesn't match a configured server_name block, NGINX will either serve the default server certificate (causing a browser mismatch error) or drop the connection if configured strictly.
2. The Caching Conundrum: [CORRECT] Excellent. Because the header contains private, NGINX's default behavior is to protect user privacy by refusing to cache it. Every subsequent request will remain a MISS, passing straight to the backend.
3. The Connection Exhaustion: [CORRECT] You nailed the core culprit: keepalive was missing, causing massive TCP socket churn (TIME_WAIT exhaustion).
4. The WebSocket Breakdown: [CORRECT] Perfect syntax. Passing Upgrade and Connection "Upgrade" is non-negotiable for the handshake to succeed.

Part 2: The Configuration Code Review
Bug 1: The WebSocket Protocol Version
Your Analysis: [CORRECT] Line 24 uses proxy_http_version 1.0;. WebSockets require HTTP/1.1 to leverage the connection upgrade mechanism.

Bug 2: NGINX Plus vs. Open Source Health Checks
Your Analysis: [CORRECT] Outstanding catch! The check inter=2s directive belongs to NGINX Plus (the paid enterprise version) or requires compiling a third-party module. In standard Open Source NGINX, you must use passive parameters like max_fails=3 fail_timeout=10s.

Bug 3: The Broken Upstream Keepalive (Nuance Check)
Your Analysis: [PARTIALLY CORRECT / GOOD EFFORT] You noticed the conflict around keepalive 16; on line 8.
The Technical Reality: ip_hash and keepalive can actually coexist in NGINX. The true fatal bug here is a silent configuration failure. For keepalive 16; to actually function, you must append two headers inside the location blocks using that upstream:

```nginx
proxy_http_version 1.1;
proxy_set_header Connection "";
```