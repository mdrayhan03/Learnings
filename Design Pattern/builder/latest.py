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
        product = self.computer
        self.reset()  # Clear the builder so it's ready for the next PC
        return product

# --- The Messy Way ---
# Hard to read: what is "32"? What is "1TB"?
my_pc = ComputerBuilder().add_cpu("Intel i9").add_ram("32GB").add_storage("1TB").add_gpu("RTX 4090").add_screen("4K").add_keyboard("Mechanical").build()
print(my_pc)

# What if I only want a basic office PC? I have to pass a lot of Nones or know the order.
office_pc = ComputerBuilder().add_cpu("i3").add_ram("8GB").add_storage("256GB").add_keyboard("Standard").build()
print(office_pc)