class Cash:
    def __init__(self, amount):
        self._amount = amount

    def remove(self, amount):
        self._amount -= amount

class Wallet:
    def __init__(self, cash: Cash):
        self._cash = cash

    def get_cash(self) -> Cash:
        return self._cash

class Customer:
    def __init__(self, wallet: Wallet):
        self._wallet = wallet

    def get_wallet(self) -> Wallet:
        return self._wallet

# --- The Violation ---
customer = Customer(Wallet(Cash(100)))

# Look at this train wreck chain. The client knows way too much about the internal structure!
customer.get_wallet().get_cash().remove(20) 
print("Paid successfully!")