from abc import ABC, abstractmethod

# 1. The Product Interface
class Transport(ABC) :
    @abstractmethod
    def deliver(self) :
        pass

# 2. Concrete Products
class Truck(Transport):
    def __init__(self, license_number, capacity):
        self.license_number = license_number
        self.capacity = capacity

    def deliver(self):
        return "Delivering by land in a box."

class Ship(Transport):
    def deliver(self):
        return "Delivering by sea in a container."

# 3. The Creator (The "Factory" Logic)
class Logistics(ABC) :
    @abstractmethod
    def create_transport(self, **filters) -> Transport :
        pass

    def plan_delivery(self, **filters) :
        transport = self.create_transport(**filters)
        return transport.deliver()
    
class RoadLogistics(Logistics) :
    def create_transport(self, **filters):
        weight_needed = filters.get("weight", 1000)
        region = filters.get("region", "Dhaka")
        return Truck(license_number="BD-123", capacity=weight_needed)

class SeaLogistics(Logistics) :
    def create_transport(self):
        return Ship()
    
# 4. Concrete Creators
def client_code(logistics: Logistics, **filters):
    print(f"Client: I'm not aware of the logistics class, but it works.")
    print(logistics.plan_delivery(**filters))

# Execution
print("App: Launched with RoadLogistics.")
# 1. Instantiate the manager
road_mgr = RoadLogistics() 
# 2. Pass the manager AND the specific requirements to the client
client_code(road_mgr, weight=5000, region="Chittagong")

print("\nApp: Launched with SeaLogistics.")
sea_mgr = SeaLogistics()
client_code(sea_mgr)