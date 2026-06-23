from abc import ABC, abstractmethod
import heapq

class ParkingSpot(ABC): 
    def __init__(self, floor, spot_number):
        self.floor = floor  # This is a Floor object
        self.spot_number = spot_number
        self.spot_type = None
        self.is_free = True

    # Python uses __lt__ (less than) to compare objects using min() or heapq
    def __lt__(self, other):
        if self.floor.floor_no == other.floor.floor_no:
            return self.spot_number < other.spot_number
        return self.floor.floor_no < other.floor.floor_no

# Added proper inheritance (ParkingSpot) here:
class CompactSpot(ParkingSpot):
    def __init__(self, floor, spot_number):
        super().__init__(floor, spot_number)
        self.spot_type = "compact"
        

class MediumSpot(ParkingSpot):
    def __init__(self, floor, spot_number):
        super().__init__(floor, spot_number)
        self.spot_type = "medium"
    
class LargeSpot(ParkingSpot):
    def __init__(self, floor, spot_number):
        super().__init__(floor, spot_number)
        self.spot_type = "large"

class Floor: 
    def __init__(self, floor_no: int):
        self.floor_no = floor_no
        self.parking_spots = [] # Renamed to plural for clarity
        self.free_spots = {}

    def add_parking_spot(self, parking_spot: ParkingSpot):
        spot_type = parking_spot.spot_type
        if spot_type not in self.free_spots:
            self.free_spots[spot_type] = []
        
        # Use heappush to maintain the min-heap property automatically 
        # Python uses the __lt__ method we defined in ParkingSpot to sort them!
        heapq.heappush(self.free_spots[spot_type], parking_spot)
        self.parking_spots.append(parking_spot)


class FloorRepository:
    def __init__(self):
        self.floors = {}

    def add_floor(self, floor: Floor):
        self.floors[floor.floor_no] = floor
        

class Vehicle(ABC): 
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.vehicle_type = None
        self.allowed_spot = []

class Truck(Vehicle):
    def __init__(self, vehicle_id):
        super().__init__(vehicle_id)
        self.vehicle_type = "truck"
        self.allowed_spot = ["large"]

class Car(Vehicle):
    def __init__(self, vehicle_id):
        super().__init__(vehicle_id)
        self.vehicle_type = "car"
        self.allowed_spot = ["medium", "large"]

class Bike(Vehicle):
    def __init__(self, vehicle_id):
        super().__init__(vehicle_id)
        self.vehicle_type = "bike"
        self.allowed_spot = ["compact", "medium", "large"]

class ParkingTicket: 
    @staticmethod
    def make_ticket(parking_spot: ParkingSpot, vehicle: Vehicle):
        ticket = f"===Parking Ticket===\nVehicle No: {vehicle.vehicle_id}\nParking Spot No: {parking_spot.spot_number}\nParking Type: {parking_spot.spot_type}\n===Parking Ticket==="
        return ticket
        
class ParkingLot: 
    def __init__(self, floor_repo: FloorRepository):
        self.floor_repo = floor_repo

    def park_vehicle(self, vehicle: Vehicle):
        allowed_spots = vehicle.allowed_spot
        floors = self.floor_repo.floors.values()

        for floor in floors:
            for allowed_spot in allowed_spots:
                heap = floor.free_spots.get(allowed_spot, [])

                # O(1) Check: Is there an available spot in this heap?
                # We also peek at the top element to make sure it wasn't manually invalidated
                while heap:
                    # Look at the closest spot without removing it yet
                    closest_spot = heap[0] 
                    
                    if closest_spot.is_free:
                        # O(log N) Removal: Safely pop the absolute best spot off the heap
                        heapq.heappop(heap)
                        
                        # Mark it occupied
                        closest_spot.is_free = False
                        
                        ticket = ParkingTicket.make_ticket(closest_spot, vehicle)
                        print(f"Vehicle {vehicle.vehicle_id} parked at spot {closest_spot.spot_number} on floor {floor.floor_no}")
                        return ticket
                    else:
                        # Stale spot (already taken somehow), clear it out of the heap
                        heapq.heappop(heap)
                        
        print(f"No available spots found for vehicle {vehicle.vehicle_id}")
        return None
    
# --- SIMULATION RUNNER ---
if __name__ == "__main__":
    # 1. Setup the Repository and Floors
    repo = FloorRepository()
    
    floor1 = Floor(floor_no=1)
    floor2 = Floor(floor_no=2)
    
    repo.add_floor(floor1)
    repo.add_floor(floor2)
    
    # 2. Populate Floor 1 with spots
    # Floor 1 has 1 Compact, 1 Medium, and 1 Large spot
    floor1.add_parking_spot(CompactSpot(floor=floor1, spot_number=101))
    floor1.add_parking_spot(MediumSpot(floor=floor1, spot_number=102))
    floor1.add_parking_spot(LargeSpot(floor=floor1, spot_number=103))
    
    # 3. Populate Floor 2 with spots
    # Floor 2 has 1 Medium and 1 Large spot
    floor2.add_parking_spot(MediumSpot(floor=floor2, spot_number=201))
    floor2.add_parking_spot(LargeSpot(floor=floor2, spot_number=202))
    
    # 4. Initialize the Parking Lot system
    parking_lot = ParkingLot(repo)
    
    # 5. Create a fleet of incoming vehicles
    vehicles = [
        Bike("BIKE-99"),  # Can fit anywhere, should prefer compact first
        Car("CAR-01"),    # Can fit medium or large
        Truck("TRUCK-7"), # Can ONLY fit large
        Car("CAR-02"),    # Needs medium or large
        Bike("BIKE-00")   # Late arrival
    ]
    
    print("--- Starting Parking Lot Simulation ---\n")
    
    # 6. Simulate parking each vehicle
    tickets = []
    for vehicle in vehicles:
        print(f"Attempting to park {vehicle.vehicle_type.upper()} (ID: {vehicle.vehicle_id})...")
        ticket = parking_lot.park_vehicle(vehicle)
        if ticket:
            tickets.append(ticket)
        print("-" * 40)
        
    print("\n--- Generated Tickets Summary ---")
    for t in tickets:
        print(t)
        print()