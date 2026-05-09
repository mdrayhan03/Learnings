class Computer:
    def __init__(self, cpu, ram, storage, gpu=None, screen=None, keyboard=None):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.screen = screen
        self.keyboard = keyboard

    def __str__(self):
        return f"Computer: [CPU: {self.cpu}, RAM: {self.ram}, GPU: {self.gpu}]"

# --- The Messy Way ---
# Hard to read: what is "32"? What is "1TB"?
my_pc = Computer("Intel i9", "32GB", "1TB", "RTX 4090", "4K", "Mechanical")
print(my_pc)

# What if I only want a basic office PC? I have to pass a lot of Nones or know the order.
office_pc = Computer("i3", "8GB", "256GB", None, None, "Standard")
print(office_pc)