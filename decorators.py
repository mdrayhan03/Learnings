import time
from functools import wraps

def timeit_with_message(message="Operation"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            print(f"[TIMER] {message} -> took {elapsed:.6f} seconds")
            return result, elapsed
        return wrapper
    return decorator