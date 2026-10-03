### Input
```bash
# 1. Start Docker environment
docker-compose up -d

# 2. Seed 3 distinct users into Redis
# User 1: Enterprise Tier
docker exec -it gateway_cache_7_4 redis-cli SET key:key_ent '{"user": "Corp_CEO", "tier": "enterprise"}'

# User 2: Standard user whose CRC32 hash falls into the 20% Canary bucket
docker exec -it gateway_cache_7_4 redis-cli SET key:key_user_a '{"user": "User_2", "tier": "free"}'

# User 3: Standard user whose CRC32 hash falls into the 80% Stable bucket
docker exec -it gateway_cache_7_4 redis-cli SET key:key_user_b '{"user": "User_1", "tier": "free"}'

# 3. TEST 1: Enterprise User (Always hits enterprise cluster)
curl -s -H "apikey: key_ent" http://localhost:8000/api/v1/data

# 4. TEST 2: Canary User_2 (Execute 5 times - ALWAYS hits Canary v2.0.0)
for i in {1..5}; do curl -s -H "apikey: key_user_a" http://localhost:8000/api/v1/data; echo ""; done

# 5. TEST 3: Stable User_1 (Execute 5 times - ALWAYS hits Stable v1.0.0)
for i in {1..5}; do curl -s -H "apikey: key_user_b" http://localhost:8000/api/v1/data; echo ""; done
```