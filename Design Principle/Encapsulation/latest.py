class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance  # PROBLEM: Completely public and unprotected

    @property
    def balance(self) -> float :
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        if value < 0 :
            raise ValueError("Transaction aborted: Balance cannot be negative!")
        self._balance = value

# --- Usage ---
try:
    account = BankAccount("Alice", 100)
    print(f"Initial Balance: ${account.balance}") # Accesses the getter
    
    # Let's try to break the system now
    account.balance = -999999  # Triggers the setter!
except ValueError as e:
    print(f"Error caught successfully: {e}")

print(f"Final safe balance: ${account.balance}")