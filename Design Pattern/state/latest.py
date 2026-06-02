from abc import ABC, abstractmethod

class VendingMachine:
    def __init__(self):
        # Initialize all possible states
        self.no_money = NoMoneyState(self)
        self.has_money = HasMoneyState(self)
        self.sold_out = SoldOutState(self)
        
        # Current state
        self._state = self.no_money

    def set_state(self, state):
        self._state = state

    # The machine's actions just delegate to the current state
    def insert_money(self):
        self._state.insert_money()

    def press_button(self):
        self._state.press_button()

class State(ABC) :
    @abstractmethod
    def insert_money(self) : pass

    @abstractmethod
    def press_button(self) : pass

class NoMoneyState(State):
    def __init__(self, machine):
        self.machine = machine

    def insert_money(self):
        print("Money inserted! You can now press the button.")
        self.machine.set_state(self.machine.has_money) # Transition!
        
    def press_button(self):
        print("Error: You need to insert money first.")

class HasMoneyState(State):
    def __init__(self, machine):
        self.machine = machine

    def insert_money(self):
        print("Error: Money is already in the slot.")
        
    def press_button(self):
        print("Dispensing drink... Enjoy!")
        # Logic for inventory check could go here
        self.machine.set_state(self.machine.no_money) # Transition back!

class SoldOutState(State) :
    def __init__(self, machine):
        self.machine = machine
        
    def insert_money(self):
        print("Machine sold out.")
        
    def press_button(self):
        print("Machine sold out.")

# --- Execution ---
vm = VendingMachine()

vm.press_button()   # Error: Insert money first
vm.insert_money()   # Money inserted!
vm.press_button()   # Dispensing...
vm.press_button()