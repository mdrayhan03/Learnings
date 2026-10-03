### Input
```bash
# 1. Start Docker environment
docker-compose up -d

# 2. Seed a test user in Redis
docker exec -it gateway_cache_7_3 redis-cli SET key:my_secret_key '{"user": "Alice_73", "tier": "pro"}'

# 3. Make a request through the Gateway
curl -i -H "apikey: my_secret_key" http://localhost:8000/api/v1/data
```

### Expected Output
```bash
HTTP/1.1 200 OK
Server: API-Gateway
Content-Type: application/json

{
  "status": "success",
  "gateway_timestamp": 1711234567.89,
  "data": {
    "authenticated_as": "Alice_73",
    "correlation_id": "1711234567.89-4321",
    "message": "Welcome to the secure internal data cluster!"
  }
}
```