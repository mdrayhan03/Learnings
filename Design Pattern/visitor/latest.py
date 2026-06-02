from abc import ABC, abstractmethod

class House:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor) :
        return visitor.visit_house(self)

class Bank:
    def __init__(self, gold_reserve):
        self.gold_reserve = gold_reserve

    def accept(self, visitor) :
        return visitor.visit_bank(self)
    
class Visitor(ABC) :
    @abstractmethod
    def visit_house(self, instance) : pass

    @abstractmethod
    def visit_bank(self, instance) : pass

class InsuranceVisitor(Visitor) :
    def visit_house(self, instance) : 
        return instance.value * 0.05

    def visit_bank(self, instance) : 
        return instance.gold_reserve * 0.01
    
class TaxVisitor(Visitor) :
    def visit_house(self, instance) : 
        return instance.value * 0.02

    def visit_bank(self, instance) : 
        return instance.gold_reserve * 0.08
    
house = House(200000)
bank = Bank(1000000)

insurance = InsuranceVisitor()
tax = TaxVisitor()

print(f"House Risk: {house.accept(insurance)}")
print(f"Bank Tax: {bank.accept(tax)}")