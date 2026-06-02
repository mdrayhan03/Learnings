from abc import ABC, abstractmethod

class Beverage(ABC) :
    def boil_water(self) :
        print("Boiling water...")

    @abstractmethod
    def brew(self) :
        pass
    
    def pour_in_cup(self) :
        print("Pouring into cup...")

    @abstractmethod
    def add_condiments(self) :
        pass

    def prepare_recipe(self) :
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()

class Tea(Beverage):
    def brew(self):
        print("Steeping the tea...")

    def add_condiments(self):
        print("Adding Lemon.")

class Coffee(Beverage):
    def brew(self):
        print("Dripping coffee through filter...")

    def add_condiments(self):
        print("Adding Sugar and Milk.")

# Execution
my_tea = Tea()
my_tea.prepare_recipe()
print()
my_coffee = Coffee()
my_coffee.prepare_recipe()