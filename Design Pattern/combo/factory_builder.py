class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.screen = None
        self.keyboard = None
    def __str__(self):
        return f"Computer: [CPU: {self.cpu}, RAM: {self.ram}, GPU: {self.gpu}]"

class ComputerBuilder() :
    def __init__(self) :
        self.computer = Computer()

    def add_cpu(self, cpu) :
        self.computer.cpu = cpu
        return self
    
    def add_ram(self, ram) :
        self.computer.ram = ram
        return self

    def add_storage(self, storage) :
        self.computer.storage = storage
        return self

    def add_gpu(self, gpu) :
        self.computer.gpu = gpu
        return self

    def add_screen(self, screen) :
        self.computer.screen = screen
        return self

    def add_keyboard(self, keyboard) :
        self.computer.keyboard = keyboard
        return self
    
    def build(self) :
        return self.computer
    
# Factory 
from abc import ABC, abstractmethod

class ComputerFactory(ABC) :
    @abstractmethod
    def create_computer(self):
        pass

    def build_computer(self) :
        computerbuilder = self.create_computer()
        computer = computerbuilder.build()
        return computer
    
class HomeComputerFactory(ComputerFactory) :
    def create_computer(self):
        return (ComputerBuilder().add_cpu("Intel i9")
                    .add_ram("32GB")
                    .add_storage("1TB")
                    .add_gpu("RTX 4090")
                    .add_screen("4K")
                    .add_keyboard("Mechanical")
                )
    
class OfficeComputerFactory(ComputerFactory) :
    def create_computer(self):
        return (ComputerBuilder().add_cpu("i3")
                    .add_ram("8GB")
                    .add_storage("256GB")
                    .add_keyboard("Standard")
                )


# Execution
home_factory = HomeComputerFactory()
office_factory = OfficeComputerFactory()

# 2. Let the Factory use the Builder to produce the object
my_home_pc = home_factory.build_computer()
my_office_pc = office_factory.build_computer()

print(f"Home Build: {my_home_pc}")
print(f"Office Build: {my_office_pc}")