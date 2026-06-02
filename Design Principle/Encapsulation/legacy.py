class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance  # PROBLEM: Completely public and unprotected

# Usage
account = BankAccount("Alice", 100)
account.balance = -999999  # Allowed! The system is broken.