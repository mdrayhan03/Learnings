class Cash:
    def __init__(self, amount):
        self._amount = amount

    def remove(self, amount):
        self._amount -= amount

class Wallet:
    def __init__(self, cash: Cash):
        self._cash = cash
    
    def pay(self, amount) :
        self._cash.remove(amount)

class Customer:
    def __init__(self, wallet: Wallet):
        self._wallet = wallet

    def pay(self, amount) :
        self._wallet.pay(amount)

customer = Customer(Wallet(Cash(100)))
customer.pay(20)
print("Paid successfully!")