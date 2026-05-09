class DatabaseConnection:
    _instance = None
    _initialized = False

    def __new__(cls) :
        if cls._instance is None:
            print('Creating new db connection')
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_id = id(self)
            print(f"--- Opening new DB Connection [{self.connection_id}] ---")
            DatabaseConnection._initialized = True

    def query(self, sql):
        print(f"Executing '{sql}' using connection {self.connection_id}")



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