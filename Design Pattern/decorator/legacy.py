class Coffee:
    def get_cost(self):
        return 10
    def get_description(self):
        return "Simple Coffee"

# Adding Milk
class CoffeeWithMilk(Coffee):
    def get_cost(self):
        return super().get_cost() + 2
    def get_description(self):
        return super().get_description() + ", Milk"

# Adding Sugar
class CoffeeWithSugar(Coffee):
    def get_cost(self):
        return super().get_cost() + 1
    def get_description(self):
        return super().get_description() + ", Sugar"

# WHAT IF SOMEONE WANTS BOTH? 
# We have to create a new class for the combination!
class CoffeeWithMilkAndSugar(Coffee):
    def get_cost(self):
        return 13 # 10 + 2 + 1
    def get_description(self):
        return "Simple Coffee, Milk, Sugar"

# WHAT IF SOMEONE WANTS WHIPPED CREAM?
# Now we need:
# - CoffeeWithCream
# - CoffeeWithCreamAndMilk
# - CoffeeWithCreamAndSugar
# - CoffeeWithCreamAndMilkAndSugar...

# Execution
my_order = CoffeeWithMilkAndSugar()
print(f"Order: {my_order.get_description()}")
print(f"Cost: ${my_order.get_cost()}")