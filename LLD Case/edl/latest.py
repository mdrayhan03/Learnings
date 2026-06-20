import heapq

class Elevator:
    # Define States as Class Constants to guarantee structural accuracy
    STATE_IDLE = "IDLE"
    STATE_MOVING_UP = "MOVING_UP"
    STATE_MOVING_DOWN = "MOVING_DOWN"
    STATE_DOORS_OPEN = "DOORS_OPEN"

    def __init__(self, elevator_id: int, current_floor=1):
        self.id = elevator_id
        self.current_floor = current_floor
        self.state = self.STATE_IDLE
        
        # Priority Heaps
        self.up_queue = []    # Min-Heap
        self.down_queue = []  # Max-Heap (stored as negative values)

    def add_request(self, target_floor: int):
        if target_floor > self.current_floor:
            heapq.heappush(self.up_queue, target_floor)
        else:
            heapq.heappush(self.down_queue, (-1 * target_floor))

    def step(self):
        print(f"🛗 Elevator {self.id} | Floor: {self.current_floor} | State: {self.state} | UpQueue: {self.up_queue} | DownQueue: {[abs(x) for x in self.down_queue]}")

        if self.state == self.STATE_IDLE:
            if self.up_queue:
                self.state = self.STATE_MOVING_UP
            elif self.down_queue:
                self.state = self.STATE_MOVING_DOWN
        
        elif self.state == self.STATE_MOVING_UP:
            if self.current_floor == self.up_queue[0]:
                heapq.heappop(self.up_queue)
                self.state = self.STATE_DOORS_OPEN
            elif self.current_floor < self.up_queue[0]:
                self.current_floor += 1
        
        elif self.state == self.STATE_MOVING_DOWN:
            if self.current_floor == (-1 * self.down_queue[0]):
                heapq.heappop(self.down_queue)
                self.state = self.STATE_DOORS_OPEN
            elif self.current_floor > (-1 * self.down_queue[0]):
                self.current_floor -= 1
        
        elif self.state == self.STATE_DOORS_OPEN:
            print(f"✨ [ARRIVAL] Elevator {self.id} opening doors at floor {self.current_floor}!")
            
            # SCAN evaluation loop
            if self.up_queue:
                self.state = self.STATE_MOVING_UP
            elif self.down_queue:
                self.state = self.STATE_MOVING_DOWN
            else:
                self.state = self.STATE_IDLE


class FleetController:
    def __init__(self, num_elevators=4):
        self.elevators = [Elevator(i) for i in range(1, num_elevators + 1)]

    def dispatch_request(self, pickup_floor: int):
        best_elevator = None
        lowest_cost = float('inf')

        for elevator in self.elevators:
            moving_dir = 0
            if elevator.state == Elevator.STATE_MOVING_UP:
                moving_dir = 1
            elif elevator.state == Elevator.STATE_MOVING_DOWN:
                moving_dir = -1

            # Heuristic calculation
            distance_cost = abs(elevator.current_floor - pickup_floor)
            directional_penalty = (elevator.current_floor - pickup_floor) * moving_dir
            workload_penalty = (len(elevator.up_queue) + len(elevator.down_queue)) * 4

            total_cost = distance_cost + directional_penalty + workload_penalty
            
            if total_cost < lowest_cost:
                lowest_cost = total_cost
                best_elevator = elevator

        print(f"📡 [DISPATCH] Allocating floor {pickup_floor} to Elevator {best_elevator.id} (Cost: {lowest_cost})")
        best_elevator.add_request(pickup_floor)

    def step_fleet(self):
        for elevator in self.elevators:
            elevator.step()


# --- Verification ---
if __name__ == "__main__":
    fleet = FleetController()
    
    fleet.dispatch_request(6)
    fleet.dispatch_request(3)
    
    for tick in range(1, 10):
        print(f"\n⏱️ --- SIMULATION TICK {tick} ---")
        fleet.step_fleet()