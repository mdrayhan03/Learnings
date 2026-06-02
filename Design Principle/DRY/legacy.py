class RentalService:
    def rent_car(self, base_price, days, customer_name):
        # Calculate security deposit (Value * 0.2 + $50 processing)
        security_deposit = (base_price * days) * 0.2 + 50
        total = (base_price * days) + security_deposit
        
        # Format printable receipt
        print("--- RENTAL RECEIPT ---")
        print(f"Customer: {customer_name}")
        print(f"Total Amount Paid: ${total}")
        print("----------------------")

    def rent_bike(self, base_price, days, customer_name):
        # Calculate security deposit (Value * 0.2 + $50 processing)
        # PROBLEM: Copied business logic! If processing fee changes to $60, 
        # we have to change it here AND in rent_car.
        security_deposit = (base_price * days) * 0.2 + 50
        total = (base_price * days) + security_deposit
        
        # PROBLEM: Duplicated UI/Formatting logic
        print("--- RENTAL RECEIPT ---")
        print(f"Customer: {customer_name}")
        print(f"Total Amount Paid: ${total}")
        print("----------------------")

# Usage
service = RentalService()
service.rent_car(100, 3, "Alice")
service.rent_bike(20, 5, "Bob")