import threading

def singletone(cls) :
    instances = {}
    lock = threading.Lock()
    def get_instance(*args, **kwargs) :
        if cls not in instances :
            with lock :
                if cls not in instances :
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singletone
class DatabaseConnection:
    def __init__(self):
        self.connection_id = id(self)
        print(f"--- Opening new DB Connection [{self.connection_id}] ---")

    def query(self, sql):
        print(f"Executing '{sql}' using connection {self.connection_id}")

# --- Simulation of a messy app ---

def save_user_profile():
    # New instance created here
    db = DatabaseConnection()
    db.query("INSERT INTO users VALUES ('Gemini')")

def log_activity():
    # Another new instance created here
    db = DatabaseConnection()
    db.query("INSERT INTO logs VALUES ('User logged in')")

def generate_report():
    # And another one...
    db = DatabaseConnection()
    db.query("SELECT * FROM analytics")

# Execution
save_user_profile()
log_activity()
generate_report()