class NaiveParkingSpot:
    def __init__(self, floor, spot_id, spot_type):
        self.floor = floor
        self.spot_id = spot_id
        self.spot_type = spot_type  # "COMPACT", "LARGE"
        self.is_free = True

class NaiveParkingLot:
    def __init__(self):
        # Nested layout representing 2 floors, each with 5 spots
        self.floors = [
            [NaiveParkingSpot(1, i, "COMPACT" if i < 3 else "LARGE") for i in range(1, 6)],
            [NaiveParkingSpot(2, i, "COMPACT" if i < 3 else "LARGE") for i in range(1, 6)]
        ]

    def park_vehicle(self, vehicle_type):
        # ⚠️ O(N) Naive Search Loop! Sweeps through every single array element
        for floor_idx in range(len(self.floors)):
            for spot in self.floors[floor_idx]:
                if spot.is_free and spot.spot_type == vehicle_type:
                    spot.is_free = False
                    print(f"🚗 Parked in Floor {spot.floor}, Spot {spot.spot_id}")
                    return spot
        print("❌ Parking Full!")
        return None

    def release_vehicle(self, floor, spot_id):
        # Another linear search loop to find the spot to free
        for floor_idx in range(len(self.floors)):
            for spot in self.floors[floor_idx]:
                if spot.floor == floor and spot.spot_id == spot_id:
                    spot.is_free = True
                    print(f"🔓 Freed Floor {floor}, Spot {spot_id}")
                    return