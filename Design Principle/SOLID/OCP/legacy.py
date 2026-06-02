class DiscountManager:
    def apply_discount(self, price, customer_type):
        # PROBLEM: Every time a new customer type is added (e.g., "Silver"),
        # we have to MODIFY this class. It's not "Closed for Modification".
        if customer_type == "regular":
            return price * 0.9
        elif customer_type == "vip":
            return price * 0.8
        elif customer_type == "student":
            return price * 0.7
        return price

# Usage
manager = DiscountManager()
print(manager.apply_discount(100, "vip"))