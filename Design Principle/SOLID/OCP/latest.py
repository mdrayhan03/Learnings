from abc import ABC, abstractmethod

class DiscountStrategy(ABC) :
    @abstractmethod
    def get_discount(self, price) : pass

class RegularDiscount(DiscountStrategy) :
    def get_discount(self, price):
        return price * 0.9
    
class VIPDiscount(DiscountStrategy) :
    def get_discount(self, price):
        return price * 0.8
    
class StudentDiscount(DiscountStrategy) :
    def get_discount(self, price):
        return price * 0.7
    
class DiscountManager :
    def apply_discount(self, price, discount_strategy: DiscountStrategy):
        return discount_strategy.get_discount(price)
    
# Usage
manager = DiscountManager()
print(manager.apply_discount(100, VIPDiscount()))