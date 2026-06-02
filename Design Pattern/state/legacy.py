class VendingMachine:
    def __init__(self):
        self.state = "NO_MONEY"

    def insert_money(self):
        if self.state == "NO_MONEY":
            print("Money inserted.")
            self.state = "HAS_MONEY"
        elif self.state == "HAS_MONEY":
            print("Money already there.")
        elif self.state == "SOLD_OUT":
            print("Machine sold out.")

    def press_button(self):
        if self.state == "NO_MONEY":
            print("Insert money first.")
        elif self.state == "HAS_MONEY":
            print("Dispensing...")
            self.state = "NO_MONEY"
        # Imagine 10 more states... this becomes unreadable!