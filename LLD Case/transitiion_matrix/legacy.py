class MessyVendingMachine:
    def __init__(self, stock: int):
        self.state = "IDLE"  # IDLE, HAS_COIN, DISPENSING, MAINTENANCE
        self.stock = stock
        self.balance = 0

    def insert_coin(self, amount: int):
        if self.state == "IDLE":
            if amount > 0:
                self.balance += amount
                self.state = "HAS_COIN"
                print(f"Coin accepted! Balance: ${self.balance}")
            else:
                print("Invalid coin amount.")
        elif self.state == "HAS_COIN":
            self.balance += amount
            print(f"Balance updated! Total: ${self.balance}")
        elif self.state == "DISPENSING":
            print("Error: Processing current order. Cannot accept coins.")
        elif self.state == "MAINTENANCE":
            print("Error: Machine out of order for maintenance.")

    def press_button(self):
        if self.state == "IDLE":
            print("Error: Please insert a coin first.")
        elif self.state == "HAS_COIN":
            if self.stock > 0:
                self.state = "DISPENSING"
                print("Initiating drink dispense...")
                # Simulating a sequential internal trigger
                self.complete_dispense()
            else:
                print("Out of stock! Returning coin.")
                self.balance = 0
                self.state = "IDLE"
        elif self.state == "DISPENSING":
            print("Error: Already dispensing an item.")
        elif self.state == "MAINTENANCE":
            print("Error: Out of service.")

    def complete_dispense(self):
        if self.state == "DISPENSING":
            self.stock -= 1
            self.balance = 0
            print("Item dropped safely! Enjoy your drink.")
            if self.stock > 0:
                self.state = "IDLE"
            else:
                print("Machine is now empty.")
                self.state = "MAINTENANCE"
        else:
            print("System failure: Cannot dispense outside of DISPENSING state.")

    def trigger_system_error(self):
        # Hard to safely track error routing across states
        print("🚨 Critical hardware fault detected!")
        self.state = "MAINTENANCE"

    def fix_machine(self):
        if self.state == "MAINTENANCE":
            self.stock = 10  # Restock
            self.state = "IDLE"
            print("Machine fixed and rebooted into IDLE.")
        else:
            print("Machine does not require maintenance.")

# --- Driver / Execution Simulation ---
vending = MessyVendingMachine(stock=1)
vending.insert_coin(2)
vending.press_button()  # Dispenses item, stock hits 0, enters MAINTENANCE
vending.insert_coin(1)  # Rejects cleanly because it's stuck in MAINTENANCE