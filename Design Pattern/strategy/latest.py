from abc import ABC, abstractmethod

class PaymentStrategy(ABC) :
    @abstractmethod
    def pay(self, amount) :
        pass

class CreditCardStrategy(PaymentStrategy) :
    def __init__(self):
        print("--Stripe api init--")
    
    def pay(self, amount) :
        print(f"Validating card... Charging ${amount}")

class PayPalStrategy(PaymentStrategy) :
    def __init__(self):
        print("--PayPal api init--")
    
    def pay(self, amount) :
        print(f"Redirecting to PayPal... Charging ${amount}")

class BitcoinStrategy(PaymentStrategy) :
    def __init__(self):
        print("--Bitcoin api init--")
    
    def pay(self, amount) :
        print(f"Generating wallet address... Charging ${amount}")

class Order :
    def __init__(self, amount):
        print("--Place Order--")
        self.amount = amount

    def pay(self, paymentStrategy: PaymentStrategy) :
        paymentStrategy.pay(self.amount)

order = Order(100)
order.pay(CreditCardStrategy())
order.pay(PayPalStrategy())