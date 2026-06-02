class CoffeeMaker:
    def prepare(self):
        print("Boiling water...")
        print("Dripping coffee through filter...")
        print("Pouring into cup...")
        print("Adding sugar and milk...")

class TeaMaker:
    def prepare(self):
        print("Boiling water...")
        print("Steeping the tea...")
        print("Pouring into cup...")
        print("Adding lemon...")

coffee = CoffeeMaker()
coffee.prepare()

print()

tea = TeaMaker()
tea.prepare()