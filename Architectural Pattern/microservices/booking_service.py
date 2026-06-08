import json

from user_service import UserService

class Booking :
    def __init__(self, booking_id: int, user_id: int, destination: str):
        self.booking_id = booking_id
        self.user_id = user_id
        self.destination = destination

class BookingRepository :
    def __init__(self):
        self._db = {}

    def save(self, booking: Booking) :
        self._db[booking.booking_id] = booking
    
    def get_by_id(self, booking_id: int) -> Booking :
        return self._db.get(booking_id)
    
class BookingService :
    def __init__(self, booking_repo: BookingRepository, user_service: UserService):
        self.booking_repo = booking_repo
        self.user_service = user_service

    def create_booking(self, booking_id: int, user_id: int, destination: str) :
        endpoint_url = f"/internal/user/{user_id}"
        
        try:
            # 2. Make the simulated network call to the independent UserService
            response_raw = self.user_service.receive_internal_network_call(endpoint_url)
            response_data = json.loads(response_raw)
            
            # 3. Verify if the user exists based on the distributed response
            if response_data.get("status") != "200 OK" or not response_data.get("payload"):
                return json.dumps({"status": "400 Bad Request", "error": f"Booking failed. User {user_id} does not exist."}, indent=2)
            
            # 4. If user is valid, safely instantiate and save the Booking entity
            new_booking = Booking(booking_id, user_id, destination)
            self.booking_repo.save(new_booking)
            
            return json.dumps({
                "status": "201 Created",
                "message": f"Booking {booking_id} confirmed for user '{response_data['payload']['name']}' to {destination}!"
            }, indent=2)
            
        except AttributeError:
            # Catches if the user doesn't exist and user.user_id throws an error in UserService
            return json.dumps({"status": "404 Not Found", "error": f"User verification failed. ID {user_id} not found on network."}, indent=2)
        except Exception as e:
            return json.dumps({"status": "500 Internal Server Error", "error": str(e)}, indent=2)