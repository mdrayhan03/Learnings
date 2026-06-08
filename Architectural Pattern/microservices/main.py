from user_service import User, UserRepository, UserService
from booking_service import Booking, BookingRepository, BookingService

# =====================================================================
# SIMULATION DRIVER (The Orchestrator)
# =====================================================================
if __name__ == "__main__":
    print("--- Initializing Distributed Microservices Simulation ---")
    
    # 1. Setup User Microservice & populate data
    user_repo = UserRepository()
    user_service = UserService(user_repo)
    user_repo.save(User(user_id=7, name="Alice Smith", rating=4.9))
    
    # 2. Setup Booking Microservice & inject the User network client wire
    booking_repo = BookingRepository()
    booking_service = BookingService(booking_repo, user_service)
    
    print("Services are live.\n")

    # -----------------------------------------------------------------
    # TEST 1: User Exists (Successful Booking)
    # -----------------------------------------------------------------
    print("--- TEST 1: Booking for an Existing User (ID: 7) ---")
    result_1 = booking_service.create_booking(booking_id=5001, user_id=7, destination="Paris")
    print(result_1)
    print("-" * 60)

    # -----------------------------------------------------------------
    # TEST 2: User Does Not Exist (Failed Booking)
    # -----------------------------------------------------------------
    print("\n--- TEST 2: Booking for a Missing User (ID: 99) ---")
    result_2 = booking_service.create_booking(booking_id=5002, user_id=99, destination="Tokyo")
    print(result_2)
    print("-" * 60)