# Phase 1: Networking Foundations (The Theory)

## The OSI Model: Layer 4 vs Layer 7
The Open Systems Interconnection (OSI) model describes how data moves from one computer to another.

### Layer 4 (Transport Layer)
Layer 4 deals purely with delivery. It doesn't care about what data is inside in the packet; it only looks at the IP addresses and Port Numbers.
* **Protocols used:** TCP (Transmission Control Protocol) and UDP (User Datagram Protocol).
* **How a Layer 4 Load Balancer Works:** It receives a packet destined for 192.168.1.10:443, looks at its pool of backend servers, and changes the destination IP to 10.0.0.5:443. It operates purely at the packet level.
* **Pros/Cons:** It is incredibly fast and memory-efficient because it never decrypts or reads your data. However, it is "blind" - it cannot route traffic based on cookies, URLs, or headers.

### Layer 7 (Application Layer)
Layer 7 deals with the content of the data. It understands the actual application language being spoken.
* **Protocols used:** HTTP, HTTPS, FTP, SMTP.
* **How a Layer 7 Proxy/Load Balancer works:** It actually terminates (opens) the network connection. It reads the HTTP headers, looks at the cookie, and looks at the URL path (e.g., /api/v1/users).
* **Pros/Cons:** It is highly intelligent. It can route traffic to different Docker containers based on the URL paths or user sessions. However, it requires significantly more CPU and memory because it has to read and decrypt the data traffic.

## TCP Mechanics: The Three-Way Handshake
Because proxies manage connections, you must understand how a TCP connection starts. Computers don't just blast data at each other; they have a formal agreement sequence called the Three-Way Handshake.
1. **SYN (Synchronize):** The client sends a packet to the proxy saying, "I want to connect. Here is my initial sequence number."
2. **SYN-ACK (Synchronize-Acknowledge):** The proxy responds, "I received your request. I agree to connect. Here is my sequence number."
3. **ACK (Acknowledge):** The client responds, "Got it. Connection established. Let’s send data."

**Why this matters for Reverse Proxies:**<br>
When a client connects to a reverse proxy (like NGINX), the 3-way handshake happens between the client and NGINX. Once established, NGINX opens a second, entirely separate TCP 3-way handshake with your backend application container. NGINX acts as a middleman buffer, shielding your application from dealing with raw connection management.

## The TLS/SSL Handshake
When you see https://, your traffic is encrypted. A reverse proxy's most common job is **SSL Termination**—meaning it handles the heavy math of decryption so your app doesn't have to.

When a user visits an HTTPS site, a TLS handshake occurs right after the TCP handshake:
* **Client Hello:** Client sends a list of encryption algorithms (cipher suites) it supports.
* **Server Hello & Certificate:** The proxy sends back its SSL Certificate (proving its identity) and public key.
* **Key Exchange:** The client verifies the certificate with a Trusted Certificate Authority (like Let's Encrypt). The client and proxy then securely generate a shared symmetric key.
* **Encrypted Session Started:** All future traffic is locked using that shared key.

**What is SNI (Server Name Indication)?**<br>
Imagine you host three different websites on a single NGINX container: site-a.com, site-b.com, and site-c.com. Each has its own unique SSL certificate.

Because the TLS handshake happens before the HTTP request is read, how does NGINX know which certificate to show the client?

SNI solves this. It forces the client's browser to include the hostname (site-a.com) in the very first "Client Hello" packet, allowing the proxy to serve the correct certificate before decryption even happens.

## DNS-Based Load Balancing (The Entry Point)
Before traffic even reaches your servers, DNS can act as a very primitive, high-level load balancer.

When you purchase a domain, you point it to an IP address using an A-Record. If your site grows, you can map a single domain to multiple IP addresses in your DNS settings:

* example.com -> 192.168.1.50 (Server A)
* example.com -> 192.168.1.51 (Server B)

When a browser asks for example.com, the DNS server hands back those IPs in a alternating cycle (DNS Round Robin).

### The Problem with DNS Balancing:
DNS servers and web browsers aggressively cache IP addresses. If Server A crashes, the DNS provider might stop giving out its IP, but users who have it cached in their browsers will continue hitting the dead server for hours, getting a "Site Cannot Be Reached" error.

This is why we use DNS only to route traffic to highly available Load Balancers/Proxies, which then handle routing to the final application servers dynamically.

# Phase 2: Forward Proxies
While a Reverse Proxy protects and sits in front of servers, a Forward Proxy sits in front of clients (users). It acts as a middleman between a private local network and the wild internet.

## Why Do We Use Forward Proxies?
If you are inside a big company or a university, you are almost certainly using a forward proxy right now without knowing it. They are used for three main reasons:
* **Anonymity & Privacy:** Instead of your computer reaching out to google.com directly, your computer asks the forward proxy to fetch Google for you. Google only sees the IP address of the proxy, hiding your internal IP address.
* **Content Filtering & Security:** A company can configure the forward proxy to inspect outbound requests. If an employee tries to visit a malicious site, the proxy blocks the connection before it ever leaves the building.
* **Caching:** If 500 employees all download the same large software update, the forward proxy downloads it once, caches it locally, and serves it to the other 499 employees instantly at local network speeds.

## Types of Forward Proxies
When setting these up, you will encounter three levels of anonymity:
* **Transparent Proxy:** It tells the destination server exactly who you are. It passes your real IP in an HTTP header called X-Forwarded-For. (Mostly used by schools/companies just for content filtering and caching, not privacy).
* **Anonymous Proxy:** It hides your real IP from the destination server, but it explicitly admits that it is a proxy.
* **Elite / High Anonymity Proxy:** It completely hides your IP and masks itself so perfectly that the destination server has no idea a proxy is even being used.

## Hands-On Step: Let's Build One with Docker
Since you know Docker, the absolute best way to understand a forward proxy is to spin one up locally. The industry standard tool for this is called Squid.

### Step A: The Setup
Create a folder on your machine and create a basic file named squid.conf. This configuration file tells the proxy who is allowed to use it and what rules to enforce.
```nginx
# squid.conf
# Allow anyone on the local network to use this proxy
acl localnet src 0.0.0.0/0
http_access allow localnet

# Block a specific domain (Example: blocking a site)
acl blocked_sites dstdomain .badsite.com
http_access deny blocked_sites

# Open the proxy on port 3128
http_port 3128
```

### Step B: Run it via Docker
Run the following command in your terminal to start your own forward proxy container, mounting your configuration file:
```
docker run -d --name my_forward_proxy \
  -v $(pwd)/squid.conf:/etc/squid/squid.conf \
  -p 3128:3128 \
  ubuntu/squid:latest
```

### Step C: Test It
Your proxy is now running on localhost:3128. You can test it using curl in your terminal to force your traffic through your new proxy container:
```
# This should work perfectly
curl -x http://localhost:3128 https://www.google.com

# This should be blocked by your proxy rule!
curl -x http://localhost:3128 http://www.badsite.com
```

## Free Online tools to simulate Forward Proxy
| Tool Name | Type | Primary Use / Simulation Scenario |
| :--- | :--- | :--- |
| **HTTPBin** (`httpbin.org`) | Web-Based API Echo Server | Simulating how proxies modify, mask, or inject network headers (`X-Forwarded-For`, `X-Real-IP`) and checking IP masking. |
| **RequestBin** (`requestbin.com`) | Web-Based Request Inspector | Creating a public endpoint to send proxy traffic to, allowing you to inspect live TCP bodies, cookies, and headers on a dashboard. |
| **Mermaid.js Live Editor** | Web-Based Architecture Modeler | Visually mapping and drawing sequence diagrams of network requests traveling from clients through proxies to backend containers. |
| **CodeCrafters** | Interactive Learning Platform | Simulating network traffic against a custom-written proxy or server to test compliance with HTTP specifications. |
| **Wireshark** | Desktop Packet Analyzer | Capturing live network traffic on local/Docker network interfaces to visually break down the TCP 3-Way Handshake and TLS Handshake. |
| **Postman / Hoppscotch** | Desktop / Web API Client | Simulating application traffic by routing explicit HTTP/HTTPS API payloads through a custom proxy port to test latency and routing. |

# Phase 3: Reverse Proxies & NGINX Mastery
Now we are flipping the mirror. While a forward proxy protects the client, a Reverse Proxy sits in front of one or more servers. It intercepts all incoming public internet requests and routes them safely to your internal application containers.

For a modern web stack, a reverse proxy handles security, SSL/TLS decryption, and caching, meaning your backend apps (Node.js, Python, Go) can focus purely on business logic.

## NGINX Architecture vs. The Competition
NGINX is the absolute king of reverse proxies. To understand why, you have to understand how it handles traffic compared to older web servers like Apache.

* **Apache (Process-per-request):** Every time a user connects, Apache creates a brand-new computer process or thread. If 10,000 people connect at the same time, your server runs out of RAM and crashes under the weight of 10,000 open processes.

* **NGINX (Event-driven, asynchronous):** NGINX uses a master process that controls a few small "worker processes." Instead of creating a new thread for every user, a single worker process handles thousands of connections simultaneously using a continuous loop (an event loop). It says, "Give me a packet, I'll forward it. Next! Give me another packet, I'll forward it. Next!" This is why NGINX can handle massive traffic while using almost zero RAM.

## Anatomy of an nginx.conf File
When you configure NGINX, everything is controlled by a configuration file organized into cascading sections called blocks.

Here is what the basic structure looks like:
```nginx
# Main Context (Global settings like worker processes and logs)
worker_processes auto;
error_log /var/log/nginx/error.log;

events {
    # How many connections can a single worker handle?
    worker_connections 1024;
}

http {
    # HTTP Context (Settings for web traffic, mime types, compression)
    include /etc/nginx/mime.types;
    
    server {
        # Server Context (Defines a specific virtual host / website)
        listen 80;
        server_name mysite.com;

        location / {
            # Location Context (Defines what to do with specific URL paths)
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
```

## Core Reverse Proxy Features
To act as a reverse proxy, you primarily live inside the location context using specific directives.

### The proxy_pass Directive
This is the magic line that forwards traffic. If a user goes to your domain, NGINX catches it and sends it directly to your internal application container.
```nginx
server {
    listen 80;
    server_name api.mysite.com;

    location / {
        # Forwards all traffic to an internal container named 'my-node-app' running on port 3000
        proxy_pass http://my-node-app:3000;
    }
}
```

### Header Manipulation (The Proxy Identity Problem)
Because the reverse proxy stands in the middle, your backend application container only sees requests coming from one place: the proxy's internal IP address. If you check your app logs, every user looks like they have the exact same IP address!

To fix this, you must explicitly tell NGINX to append the real user's details into the request headers before passing it forward:
```nginx
location / {
    proxy_pass http://my-node-app:3000;
    
    # Pass the real client IP address to the backend app
    proxy_set_header X-Real-IP $remote_addr;
    
    # Keep track of all proxy hops the client went through
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
    # Tell the backend whether the user used HTTP or HTTPS
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Pass the original host header requested by the client
    proxy_set_header Host $host;
}
```

### SSL/TLS Termination
Instead of making your Node.js or Python app manage SSL certificates, cryptography keys, and CPU-heavy decryption, you let NGINX handle it. Traffic from the internet to NGINX is encrypted (HTTPS). Traffic from NGINX to your internal containers is plain text (HTTP), which is safe because it stays inside your isolated private network.
```nginx
server {
    listen 443 ssl; # Listen on the secure port
    server_name mysite.com;

    # Point to your SSL Certificate files
    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    # Secure protocols to use
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://my-node-app:3000;
    }
}
```

## Hands-On Docker Assignment: The Secure Web Shell
Let’s put this directly into practice using Docker Compose. We are going to build an architecture where a web app container is hidden entirely from the public, and an NGINX container acts as its secure gatekeeper.

### Step 1: Create a Project Folder
Create a folder named nginx-reverse-proxy on your machine.

### Step 2: Create the nginx.conf File
Inside that folder, create a subfolder named nginx, and place this file inside it as default.conf:
```nginx
# nginx/default.conf
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://backend-app:5000; # Targets the app container by name
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Step 3: Create the docker-compose.yml File
In your main project folder, create your compose file:
```yaml
version: '3.8'

services:
  # 1. The Gateway (Reverse Proxy)
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80" # Exposed to the public internet/your host
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend-app

  # 2. The Internal Hidden Web App (Using HTTPBin for echo verification)
  backend-app:
    image: kennethreitz/httpbin
    # Notice: NO "ports" block here. This container is completely invisible 
    # to your host machine except through the NGINX proxy.
```

### Step 4: Run It
Open your terminal inside the project folder and run:
```bash
docker compose up -d
```

### Step 5: Verify the Header Injection
Open your web browser or run curl to hit your localhost:
```bash
curl http://localhost/headers
```

Look closely at the output JSON. Even though you requested it from NGINX, the backend application will output the headers, showing that X-Real-IP and X-Forwarded-For were injected successfully by NGINX!

# Reverse Proxy Protect Backend App
## Hiding Your Backend's Identity (Obfuscation)
Without a reverse proxy, your backend application must be exposed directly to the public internet on an open port.

* **The Risk:** Attackers can run port scans to figure out exactly what server framework and version you are running (e.g., Express.js v4.17). If that specific version has a known security vulnerability (CVE), the attacker can exploit it directly.

* **The Proxy Defense:** The reverse proxy sits on the edge, exposing only standard ports (80 for HTTP, 443 for HTTPS). Your backend apps live on an isolated internal network (like a private Docker network) with no public ports open. Attackers cannot scan, see, or directly attack your application containers because they simply do not exist to the outside world.

## SSL/TLS Termination (Encrypted Traffic Management)
Managing cryptographic handshakes and SSL certificates takes significant CPU power and introduces security risks if configured incorrectly.

* **The Proxy Defense:** The reverse proxy handles the heavy math of decrypting incoming HTTPS traffic at the edge of your network. It handles the SSL certificates, enforces modern secure protocols (like TLS 1.3), and disables old, broken protocols (like SSL v3 or TLS 1.0). Once the traffic is safely decrypted, the proxy passes plain HTTP to your internal backend container over your secure, private network.

## Rate Limiting and DDoS Protection
If a malicious user or bot floods your website with 10,000 requests per second, a standard application server will quickly run out of memory, spike its CPU to 100%, and crash.

* **The Proxy Defense:** Because NGINX is event-driven and uses minimal memory, it can ingest massive amounts of simultaneous connections. You can configure NGINX to enforce Rate Limiting at the door. If a single IP address exceeds a set limit (e.g., more than 10 requests per second), NGINX drops those requests instantly with a 429 Too Many Requests error, shielding your backend app from ever seeing the traffic.

    ```nginx
    # NGINX Rate Limiting Example
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

    server {
        location /login {
            limit_req zone=mylimit burst=5; # Protects login endpoint from brute-force
            proxy_pass http://backend-app;
        }
    }
    ```
## 4. Buffering and Slowloris Attack Prevention
In a Slowloris attack, an attacker opens a connection to your server and sends HTTP data incredibly slowly (e.g., 1 byte every few seconds). A standard web server will keep that connection thread open, waiting for it to finish, until it runs out of available threads and goes down.

* **The Proxy Defense:** NGINX uses Request Buffering. When a client sends a request, NGINX waits until it has received the entire HTTP request payload in its own buffer before it ever talks to your backend. If a client is trickling data too slowly, NGINX closes the connection at the edge. Your backend app only ever receives complete, valid, fast requests.

## Request Filtering & WAF Integration
Attackers will often try to pass malicious code into your website's URL or forms to compromise your system (such as SQL Injection or Cross-Site Scripting).

* **The Proxy Defense:** You can configure a reverse proxy to parse incoming requests and block anything suspicious before it proceeds. For example, NGINX can be configured to reject requests with excessively long URLs, block specific HTTP methods you don't use (like TRACE or DELETE), or act as a Web Application Firewall (WAF) using tools like ModSecurity. If a request contains strings commonly used in database hacks (like UNION SELECT), the proxy drops it instantly.

### Summary Diagram of the Traffic Flow:
* **Malicious Traffic / Bots / DDoS:** Smashes into NGINX $\rightarrow$ Blocked by Rate Limiter/WAF $\rightarrow$ Dropped at the edge.
* **Legitimate User (HTTPS):** Handled by NGINX $\rightarrow$ SSL Decrypted $\rightarrow$ Cleaned & Verified $\rightarrow$ Safely passed to the backend application container.

# Phase 4: Load Balancers (Layer 4 & Layer 7)
Now that your backend application is safe behind an NGINX reverse proxy, imagine your e-commerce site gets hit with a massive traffic spike. A single instance of your backend container will eventually bottleneck on CPU or memory and crash.

To scale, you need to run multiple copies (instances) of your application container, and use a Load Balancer at the front gate to distribute incoming traffic evenly among them.

## Load Balancing Algorithms: How Routing Decisions are Made
When a request arrives, the load balancer uses a specific mathematical algorithm to decide which backend container should handle it.

### Round Robin (The Default)
* **How it works:** Requests are distributed sequentially down the list of servers. Request 1 goes to Container A, Request 2 goes to Container B, Request 3 goes to Container C, and Request 4 loops back to Container A.

* **Best used for:** When all your backend containers have identical hardware specs and the processing time for requests is roughly equal.

### Weighted Round Robin
* **How it works:** If you have one massive server and one small server, you can assign "weights." A server with a weight of 3 will receive three times as many requests as a server with a weight of 1.

* **Best used for:** Mixed infrastructure setups (e.g., upgrading servers gradually).

### Least Connections
* **How it works:** The load balancer looks at how many active, open connections each container is currently processing and routes the new request to the container that is least busy.

* **Best used for:** Applications where requests take a highly unpredictable amount of time to process (e.g., a query that generates a heavy PDF report vs. a quick profile fetch).

### IP Hash (Source IP Pinning)
* **How it works:** The load balancer takes the client’s IP address, runs it through a hashing function, and maps that hash to a specific server. That user's IP will always land on the exact same backend container.

* **Best used for:** Basic applications that store user login sessions in local server memory instead of a shared database (like Redis).

## The Health Check Mechanism (Self-Healing Traffic)
What happens if Container B crashes or its Docker process hangs? If the load balancer blindly keeps sending traffic to it via Round Robin, 33% of your users will get a "502 Bad Gateway" error.

To prevent this, load balancers perform Health Checks:

* **Active Health Checks:** The load balancer automatically pings a specific endpoint on your application (like GET /health) every 5 seconds. If the container responds with a 200 OK, it keeps sending traffic. If the container fails to respond or returns an error 3 times in a row, the load balancer marks it as "Dead" and routes traffic only to the remaining healthy containers.

## Hands-On Step: Load Balancing with NGINX
You can use the exact same NGINX instance you learned about in Phase 3 to act as a Load Balancer by utilizing the upstream module.

### Step A: The nginx.conf Configuration
Inside your NGINX configuration, you define an upstream block outside your server block. This block acts as your pool of containers.
```nginx
http {
    # Define the cluster of backend application containers
    upstream my_app_cluster {
        # NGINX will automatically round-robin between these three targets
        server web-app-1:5000;
        server web-app-2:5000;
        server web-app-3:5000;
    }

    server {
        listen 80;
        server_name mysite.com;

        location / {
            # Instead of a single IP, point the proxy to your upstream pool name
            proxy_pass http://my_app_cluster;
            
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## Upgrading to HAProxy (The Dedicated Heavyweight)
While NGINX handles load balancing wonderfully for most websites, enterprise-grade architectures often separate the roles: they use NGINX as the web server/reverse proxy, and HAProxy (High Availability Proxy) as a dedicated, hyper-specialized load balancer.

Why use HAProxy over NGINX?
* **Pure Performance:** HAProxy is highly optimized solely for load balancing. It handles heavy Layer 4 (TCP) routing with less CPU overhead.

* **Advanced Statistics:** It comes with a built-in interactive dashboard that shows you live metrics for every single container.

* **Deeper Health Checks:** It supports highly advanced connection checking and smoother traffic draining when you want to take a server down for maintenance.

Example HAProxy Layout:
An HAProxy configuration divides its routing rules into a frontend (where public traffic arrives) and a backend (where traffic goes).
```nginx
# haproxy.cfg
frontend my_front_gate
    bind *:80
    mode http
    default_backend my_container_pool

backend my_container_pool
    mode http
    balance roundrobin
    # 'check' enables active background health monitoring
    server web1 web-app-1:5000 check
    server web2 web-app-2:5000 check
    server web3 web-app-3:5000 check
```

## Summary: Layer 4 vs. Layer 7 Balancing Recap
Tie this back to Phase 1:

* An HAProxy Layer 4 Load Balancer can balance database traffic (like dividing read queries between 3 MySQL or PostgreSQL containers) because it only needs to look at the port.

* An NGINX Layer 7 Load Balancer can look at the cookies or path, ensuring a premium user lands on your high-speed server cluster while free users land on your standard cluster.

## Basic full implemented conf script
```nginx
http {
    upstream my_app_cluster {
        least_conn; # 1. Smartly route to the least busy container

        # 2. Monitor containers and isolate them if they crash
        server flask_app_1:5000 max_fails=3 fail_timeout=30s;
        server flask_app_2:5000 max_fails=3 fail_timeout=30s;
        server flask_app_3:5000 max_fails=3 fail_timeout=30s;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://my_app_cluster;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            
            # 3. Optional but highly recommended:
            # If a backend container throws a 502/503/504 error, NGINX immediately
            # passes the request to the next live container in the cluster before 
            # the user even notices an error.
            proxy_next_upstream error timeout http_502 http_503 http_504;
        }
    }
}
```