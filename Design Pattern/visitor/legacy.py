class House:
    def __init__(self, value):
        self.value = value

    def calculate_insurance_risk(self):
        # Business logic mixed with data
        return self.value * 0.05

    def calculate_property_tax(self):
        # More business logic mixed in
        return self.value * 0.02

class Bank:
    def __init__(self, gold_reserve):
        self.gold_reserve = gold_reserve

    def calculate_insurance_risk(self):
        # Specific logic for bank risk
        return self.gold_reserve * 0.01

    def calculate_property_tax(self):
        # Specific logic for bank tax
        return self.gold_reserve * 0.08

# Usage
house = House(200000)
bank = Bank(1000000)

print(f"House Risk: {house.calculate_insurance_risk()}")
print(f"Bank Tax: {bank.calculate_property_tax()}")