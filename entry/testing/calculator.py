# calculator.py

def apply_discount(price, discount_percentage):
    """Calculates the final price after a discount."""
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount must be between 0 and 100")
        
    discount_amount = price * (discount_percentage / 100)
    return price - discount_amount