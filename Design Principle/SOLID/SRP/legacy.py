class UserAccount:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_user_info(self):
        return f"{self.username} ({self.email})"

    def validate_email(self):
        # Logic for email validation
        if "@" in self.email:
            return True
        return False

    def save_to_database(self):
        # Database connection and saving logic
        print(f"Saving {self.username} to the database...")

# Usage
user = UserAccount("john_doe", "john@example.com")
if user.validate_email():
    user.save_to_database()