## Provision Your Users & Test
1. Build and boot up the system:

    ```bash
    docker compose up -d
    ```
2. Provision an API Key inside your running Redis cache. Let's make an active key called gold_tier_secret belonging to consumer User_101:

    ```bash
    docker exec -it gateway_cache redis-cli SET key:free_secret '{"user": "Free_User", "tier": "free"}'
    docker exec -it gateway_cache redis-cli SET key:pro_secret '{"user": "Pro_User", "tier": "pro"}'
    ```
### Test 1: Request Without a Key (Blocked)
```bash
curl -i http://localhost:8000/api/v1/data
```
- Result: HTTP 401 Unauthorized. The gateway drops the request immediately. Your Python container is never touched.

### Test 2: Request with a Valid Key (Passed)
```bash
for i in {1..12}; do curl -i -H "apikey: pro_secret" http://localhost:8000/api/v1/data; done
```
- Result: HTTP 200 OK. Notice the injected headers and the rate limit counter tracking you:

    ```http
    X-RateLimit-Limit: 3
    X-RateLimit-Remaining: 2

    {"authenticated_as":"User_101", "status":"success"...}
    ```
### Test 3: Exceeding the Rate Limit (Throttled)
Fire that exact same curl command 3 more times quickly in rapid succession:

```bash
curl -i -H "apikey: gold_tier_secret" http://localhost:8000/api/v1/data
```
- Result: On the 4th hit, the gateway enforces the subscription rules and cuts you off with an HTTP 429 Too Many Requests:

    ```http
    HTTP/1.1 429 Too Many Requests
    X-RateLimit-Remaining: 0

    {"error": "Rate limit exceeded. Upgrade your subscription tier!"}
    ```