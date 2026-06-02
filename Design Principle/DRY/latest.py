from abc import ABC, abstractmethod

class RentalService(ABC) :
    def _calculate_total_price(self, base_price, days) :
        security_deposit = (base_price * days) * 0.2 + 50
        total = (base_price * days) + security_deposit

        return total
    
    def _print_receipt(self, customer_name, total) :
        print("--- RENTAL RECEIPT ---")
        print(f"Customer: {customer_name}")
        print(f"Total Amount Paid: ${total}")
        print("----------------------")

    def rent_item(self, base_price, days, customer_name):
        total = self._calculate_total_price(base_price, days)
        self._print_receipt(customer_name, total)

class RentCar(RentalService) :
    pass

class RentBike(RentalService) :
    pass

car_service = RentCar()
car_service.rent_item(100, 3, "Alice")

bike_service = RentBike()
bike_service.rent_item(20, 5, "Bob")