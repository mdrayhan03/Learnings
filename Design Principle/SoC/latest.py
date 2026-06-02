class InventoryService :
    def __init__(self):
        # Pretend this is our raw database mock
        self.db_products = [
            {"id": 1, "name": "Desk", "price": 150, "stock": 5},
            {"id": 2, "name": "Chair", "price": 50, "stock": 12}
        ]

    def calculation(self):
        return_dict = {}
        for product in self.db_products:
            total_value = product["price"] * product["stock"]
            name = product["name"]
            return_dict[name] = total_value

        return return_dict
    
class InventoryConsoleView:
    def print_table(self, print_dict: dict) :
        print("=== INVENTORY REPORT ===")
        for p in print_dict:
            print(f"Product: {p} | Total Asset Value: ${print_dict[p]}")
        print("========================")

service = InventoryService()
products = service.calculation()

console_view = InventoryConsoleView()
console_view.print_table(products)