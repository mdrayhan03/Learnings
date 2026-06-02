from abc import ABC, abstractmethod
import threading

class VendingMachine:
    def __init__(self):
        self._state = NoMoneyState(self)

    def set_state(self, state):
        self._state = state

    # The machine's actions just delegate to the current state
    def insert_money(self):
        self._state.insert_money()

    def press_button(self):
        self._state.press_button()


def state_multiton(cls):
    # Dictionary of { (class, machine_id) : instance }
    instances = {}
    lock = threading.Lock()

    def get_instance(machine, *args, **kwargs):
        # We use the unique memory ID of the machine as the key
        key = (cls, id(machine)) 
        
        if key not in instances:
            with lock:
                if key not in instances:
                    print(f"Creating unique {cls.__name__} for Machine {id(machine)}")
                    instances[key] = cls(machine, *args, **kwargs)
        return instances[key]
    
    return get_instance

class State(ABC) :
    @abstractmethod
    def insert_money(self) : pass

    @abstractmethod
    def press_button(self) : pass

@state_multiton
class NoMoneyState(State):
    def __init__(self, machine):
        self.machine = machine

    def insert_money(self):
        print("Money inserted! You can now press the button.")
        self.machine.set_state(HasMoneyState(self.machine)) # Transition!
        
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
        self.machine.set_state(NoMoneyState(self.machine)) # Transition back!

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

# --- How it works in practice ---
vm1 = VendingMachine() # Machine A
vm2 = VendingMachine() # Machine B

vm1.insert_money() # Creates NoMoneyState for Machine A
vm2.insert_money() # Creates NoMoneyState for Machine B (separate object)

vm1.press_button() # Transitions Machine A back to NoMoneyState