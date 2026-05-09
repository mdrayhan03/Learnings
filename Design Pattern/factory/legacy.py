class Truck:
    def deliver(self):
        return "Delivering by land in a box."

class Ship:
    def deliver(self):
        return "Delivering by sea in a container."

# --- The Messy Client Code ---

def start_delivery(transport_type):
    # This is the "mess." Every time we add a 'Plane' or 'Drone', 
    # we have to change this function.
    if transport_type == "truck":
        transport = Truck()
    elif transport_type == "ship":
        transport = Ship()
    else:
        raise ValueError("Unknown transport type")
    
    print(transport.deliver())

# Execution
start_delivery("truck")
start_delivery("ship")