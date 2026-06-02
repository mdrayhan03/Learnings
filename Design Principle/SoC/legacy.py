class InventoryApp:
    def __init__(self):
        # Pretend this is our raw database mock
        self.db_products = [
            {"id": 1, "name": "Desk", "price": 150, "stock": 5},
            {"id": 2, "name": "Chair", "price": 50, "stock": 12}
        ]

    def display_inventory_report(self):
        # PROBLEM: Database access, business logic, and UI printing 
        # are all living in the exact same method.
        print("=== INVENTORY REPORT ===")
        for product in self.db_products:
            # Business logic concern (calculating asset value)
            total_value = product["price"] * product["stock"]
            
            # Presentation concern (formatting and console UI)
            print(f"Product: {product['name']} | Total Asset Value: ${total_value}")
        print("========================")