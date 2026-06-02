class PaymentProcessor:
    def process_payment(self, amount, method):
        if method == "credit_card":
            print(f"Validating card... Charging ${amount}")
        elif method == "paypal":
            print(f"Redirecting to PayPal... Charging ${amount}")
        elif method == "bitcoin":
            print(f"Generating wallet address... Charging ${amount}")
        else:
            print("Unknown method")

# The problem: Every time you add a new payment type, 
# you have to modify this core class (Breaking the Open-Closed Principle).

payment = PaymentProcessor()
payment.process_payment(1000, 'credit_card')