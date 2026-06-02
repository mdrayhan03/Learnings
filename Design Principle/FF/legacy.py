class RegistrationService:
    def register_user(self, username, email):
        # PROBLEM: Deeply nested conditions. The logic is hard to read.
        if username != "":
            if "@" in email:
                if len(username) >= 3:
                    # Actual Core Business Logic is hidden all the way down here!
                    print(f"User {username} successfully registered!")
                    return True
                else:
                    print("Error: Username must be at least 3 characters.")
                    return False
            else:
                print("Error: Invalid email format.")
                return False
        else:
            print("Error: Username cannot be empty.")
            return False