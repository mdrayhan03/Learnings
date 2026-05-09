from abc import ABC, abstractmethod

class Coffee(ABC) :
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass

class SimpleCoffee(Coffee) :
    def get_cost(self):
        return 10
    
    def get_description(self):
        return "Simple Coffee"
    

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._wrapped_coffee = coffee

    def get_cost(self):
        return self._wrapped_coffee.get_cost()

    def get_description(self):
        return self._wrapped_coffee.get_description()

class MilkDecorator(CoffeeDecorator) :
    def get_cost(self):
        return super().get_cost() + 2
    
    def get_description(self):
        return super().get_description() + ", Milk"
    
class SugarDecorator(CoffeeDecorator) :
    def get_cost(self):
        return super().get_cost() + 1
    
    def get_description(self):
        return super().get_description() + ", Sugar"
    

my_coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
print(f"Order: {my_coffee.get_description()}")
print(f"Total Cost: {my_coffee.get_cost()}tk")