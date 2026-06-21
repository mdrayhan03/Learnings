class NaiveElevator:
    def __init__(self, id):
        self.id = id
        self.current_floor = 1
        self.destination_floors = [] # Pure unsorted list (O(N) search and terrible traversal)
        self.state = "IDLE" # IDLE, MOVING

    def add_request(self, floor):
        self.destination_floors.append(floor)
        self.state = "MOVING"

    def step(self):
        if not self.destination_floors:
            self.state = "IDLE"
            return
        
        # Naively moves to the first item added to the list, passing by intermediate floors!
        target = self.destination_floors[0]
        if self.current_floor < target:
            self.current_floor += 1
            print(f"Elevator {self.id} moving UP to floor {self.current_floor}")
        elif self.current_floor > target:
            self.current_floor -= 1
            print(f"Elevator {self.id} moving DOWN to floor {self.current_floor}")
        else:
            print(f"✨ Elevator {self.id} arrived at target floor {self.current_floor}!")
            self.destination_floors.pop(0)

class NaiveFleetController:
    def __init__(self):
        self.elevators = [NaiveElevator(i) for i in range(1, 5)] # 4 Elevators

    def dispatch_request(self, pickup_floor):
        # Naive allocation: Always passes the job to the first elevator that is idle
        for e in self.elevators:
            if e.state == "IDLE":
                print(f" Allocation: Assigning floor {pickup_floor} to Elevator {e.id}")
                e.add_request(pickup_floor)
                return
        # If none are idle, dump it on elevator 1
        print(f" Allocation: All busy, forcing floor {pickup_floor} onto Elevator 1")
        self.elevators[0].add_request(pickup_floor)

# --- Simulation ---
controller = NaiveFleetController()
controller.dispatch_request(4)
controller.dispatch_request(2)