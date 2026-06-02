class RegistrationService:
    def register_user(self, username: str, email: str) -> bool:
        # Guard 1: Check for empty username
        if username == "":
            print("Error: Username cannot be empty.")
            return False

        # Guard 2: Check for invalid email
        if "@" not in email:
            print("Error: Invalid email format.")
            return False

        # Guard 3: Check for length
        if len(username) < 3:
            print("Error: Username must be at least 3 characters.")
            return False

        # --- Actual Core Business Logic ---
        # No nesting required! We only get here if all conditions passed.
        print(f"User {username} successfully registered!")
        return True

# --- Usage ---
service = RegistrationService()
service.register_user("", "test@example.com")       # Fails immediately at Guard 1
service.register_user("bob", "invalid-email")       # Fails immediately at Guard 2
service.register_user("hi", "valid@example.com")     # Fails immediately at Guard 3
service.register_user("john_doe", "john@example.com") # Success!