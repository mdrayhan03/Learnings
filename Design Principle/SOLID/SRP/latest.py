class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class EmailValidator :
    def validate_email(self, user: User):
        if "@" in user.email:
            return True
        return False
    
class UserRepository :
    def save_to_database(self, user: User):
        # Database connection and saving logic (Singleton)
        print(f"Saving {user.username} to the database...")

# execution
user = User("john_doe", "john@example.com")
email_validator = EmailValidator()
user_repository = UserRepository()

if email_validator.validate_email(user) :
    user_repository.save_to_database(user)