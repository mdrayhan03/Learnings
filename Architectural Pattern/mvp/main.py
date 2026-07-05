from abc import ABC, abstractmethod

#############
# M -> Model
#############
class UserAccountModel:
    def __init__(self, username: str, email: str):
        self.username: str = username
        self.email: str = email

class UserAccountValidator:
    @staticmethod
    def username_validation(username: str):  # Fixed: Removed self
        if len(username.strip()) == 0:        # Fixed: Corrected condition
            return False, "Username cannot be empty."
        if len(username.strip()) < 3:
            return False, f"Username -> '{username}' is less than 3 characters."
        return True, "Username validation successful."
    
    @staticmethod
    def email_validation(email: str):        # Fixed: Removed self
        if len(email.strip()) == 0:
            return False, "Email cannot be empty."
        if "@" not in email:
            return False, f"Email -> '{email}' doesn't contain '@'."
        return True, "Email validation successful."
    
class UserAccountRepository:
    def __init__(self):
        self._users = []

    def add_user(self, username: str, email: str) -> UserAccountModel:
        user = UserAccountModel(username, email)
        self._users.append(user)
        return user

############
# V -> View (Strictly Passive Interface)
############
class IUserFormView(ABC):
    @abstractmethod
    def get_username_input(self) -> str: pass

    @abstractmethod
    def get_email_input(self) -> str: pass

    @abstractmethod
    def show_validation_summary(self, message: str) -> None: pass

    @abstractmethod
    def display_success_state(self, username: str) -> None: pass

class TerminalUserFormView(IUserFormView):
    def get_username_input(self) -> str: 
        return input("Enter username: ")

    def get_email_input(self) -> str: 
        return input("Enter email: ")

    def show_validation_summary(self, message: str) -> None:
        print("\n" + "-" * 30)
        print("[VIEW ALERT] Form Validation Failed")
        print("-" * 30)
        print(f"Details: {message}\n")

    def display_success_state(self, username: str) -> None: 
        print("\n" + "-" * 30)
        print("[VIEW ALERT] Account Successfully Configured")
        print("-" * 30)
        print(f"Welcome to the platform, {username}!\n")

#################
# P -> Presenter (The Supervisor)
#################
class UserFormPresenter:
    def __init__(self, user_view: IUserFormView, user_repo: UserAccountRepository):
        self._user_view: IUserFormView = user_view
        self._user_repo: UserAccountRepository = user_repo
    
    def on_submit_clicked(self) -> None:
        # 1. Presenter actively pulls data from the passive view interfaces
        username = self._user_view.get_username_input()
        email = self._user_view.get_email_input()

        # 2. Presenter routes data to Model-side structural validators
        u_valid, u_msg = UserAccountValidator.username_validation(username)
        if not u_valid:
            self._user_view.show_validation_summary(u_msg)
            return
        
        e_valid, e_msg = UserAccountValidator.email_validation(email)
        if not e_valid:
            self._user_view.show_validation_summary(e_msg)
            return
        
        # 3. Presenter updates Model state and commands View state transformation
        user = self._user_repo.add_user(username, email)
        self._user_view.display_success_state(user.username)

#############
# Simulation
#############
if __name__ == "__main__":
    print("--- Initializing Presentation MVP Loop ---")
    view = TerminalUserFormView()
    repo = UserAccountRepository()
    presenter = UserFormPresenter(view, repo)
    
    print("Form interface ready. Triggering submission listener...\n")
    # This will prompt you for text inputs right inside your terminal console!
    presenter.on_submit_clicked()