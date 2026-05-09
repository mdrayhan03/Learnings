class RealDatabase:
    def __init__(self):
        # Imagine this takes 5 seconds to load
        print("--- Connecting to heavy Database... ---")
        self.data = {"secret_key": "12345", "user_data": "John Doe"}

    def get_data(self, key):
        return self.data.get(key)

# --- The Problem ---
# 1. This initializes even if we don't end up using it.
# 2. There is no security check.
db = RealDatabase()
print(db.get_data("secret_key"))