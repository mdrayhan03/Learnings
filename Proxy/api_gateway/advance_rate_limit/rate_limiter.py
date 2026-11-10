import math
import time

USERS = {
    "USER-101": {"tier": "basic"},
    "USER-102": {"tier": "pro"},
    "USER-103": {"tier": "max"},
}

def get_user(user_id):
    return USERS.get(user_id)

def rate_limiter_check(user_id, requested=1):
    user = get_user(user_id)

    if not user:
        return {
            "allowed": False,
            "tokens": None,
            "last_update": None,
            "retry_after": None,
        }

    capacity = 3
    refill_rate = 0.3

    if user.get("tier") == "pro":
        capacity = 5
        refill_rate = 0.5
    elif user.get("tier") == "max":
        capacity = 10
        refill_rate = 1.0

    tokens = user.get("tokens")
    last_update = user.get("last_update")
    now = time.time()

    if tokens is None or last_update is None:
        tokens = float(capacity)
        last_update = now
    else:
        # 1. Use float time differences for precise sub-second refills
        elapsed_time = now - last_update
        if elapsed_time > 0:
            generated_tokens = elapsed_time * refill_rate
            tokens = min(capacity, tokens + generated_tokens)
            last_update = now

    allowed = False
    if tokens >= requested:
        tokens -= requested
        allowed = True

    user["tokens"] = tokens
    user["last_update"] = last_update

    retry_after = 0.0
    if not allowed:
        missing_tokens = requested - tokens
        # 2. Use math.ceil to get the exact wait time in seconds
        retry_after = math.ceil(missing_tokens / refill_rate)

    return {
        "allowed": allowed,
        "tokens": math.floor(tokens),
        "last_update": last_update,
        "retry_after": retry_after,
    }

#======
# TEST
#======
user_id = "USER-101"
for i in range(10) :
    result = rate_limiter_check(user_id)
    print(f"=======HIT {i}=====\n")
    print(f"Allowed: {result.get("allowed")}\n")
    print(f"Tokens: {result.get("tokens")}\n")
    print(f"Last Update: {result.get("last_update")}\n")
    print(f"Retry After: {result.get("retry_after")}\n")
    time.sleep(0.5)