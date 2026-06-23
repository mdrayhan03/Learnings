class Seat:
    def __init__(self, row_number: int, col_index: int, seat_label: str):
        self.row_number = row_number
        self.col_index = col_index
        self.seat_label = seat_label  # e.g., "1A", "1B"
        self.is_booked = False

class SeatRow:
    def __init__(self, row_number: int, total_seats: int):
        self.row_number = row_number
        # Alphabet mapping for columns (0 -> 'A', 1 -> 'B', etc.)
        self.seats = [
            Seat(row_number, c, f"{row_number}{chr(65 + c)}") 
            for c in range(total_seats)
        ]
        # 1. FIXED CAPACITY TRACKER: Instant O(1) row feasibility boundary guard
        self.available_seats_count = total_seats

    def find_contiguous_seats_sliding_window(self, num_seats: int):
        # Step A: O(1) early exit capacity guard clause
        if self.available_seats_count < num_seats:
            return None
        
        total_seats = len(self.seats)
        
        # Step B: Slide a window of size `num_seats` across the array
        for start_col in range(total_seats - num_seats + 1):
            # Take a sub-slice of our window boundary
            window = self.seats[start_col : start_col + num_seats]
            
            # Check if all seats inside our current window are completely free
            if all(not seat.is_booked for seat in window):
                return window  # Found a contiguous chunk! Return the list of Seat objects
                
        return None
    
    def find_contiguous_seats_bitmask(self, num_seats: int):
        # Step A: O(1) capacity guard clause
        if self.available_seats_count < num_seats:
            return None
            
        total_seats = len(self.seats)
        
        # Construct a sliding consecutive target bitmask of '1's of size `num_seats`
        # Example: if num_seats=3, initial target is 0b111
        target_mask = (1 << num_seats) - 1 
        
        # Shift the target mask across the column space length
        for shift in range(total_seats - num_seats + 1):
            current_test_mask = target_mask << shift
            
            # Bitwise AND: If the intersection is 0, it means those bits are completely empty!
            if (self.row_mask & current_test_mask) == 0:
                # Map the bit positions back to our object array references
                return [self.seats[i] for i in range(shift, shift + num_seats)]
                
        return None

    def book_seats(self, seats_list: list):
        """Atomically marks seats as booked and updates the internal capacity maps"""
        for seat in seats_list:
            seat.is_booked = True
        self.available_seats_count -= len(seats_list)


class FlightSeatingEngine:
    def __init__(self, num_rows: int, seats_per_row: int):
        self.rows = [SeatRow(r + 1, seats_per_row) for r in range(num_rows)]

    def allocate_contiguous(self, requested_seats: int):
        """Scans the cabin rows to assign a block of consecutive seats together"""
        for row in self.rows:
            # Try to fetch a contiguous block from the row
            allocated_block = row.find_contiguous_seats_sliding_window(requested_seats)
            
            if allocated_block:
                # Atomically apply booking updates
                row.book_seats(allocated_block)
                labels = [seat.seat_label for seat in allocated_block]
                print(f"✈️ [BOOKED SUCCESS] Allocated {requested_seats} contiguous seats: {labels}")
                return allocated_block
                
        print(f"❌ [BOOKING FAILED] No consecutive block of {requested_seats} seats found in any row.")
        return None

    def display_cabin_map(self):
        """Renders a simple visual map of the seating capacity chart matrix"""
        print("\n--- Current Cabin Seating Map ---")
        for row in self.rows:
            row_str = f"Row {row.row_number:02d}: "
            seat_visuals = [f"[{s.seat_label}:{'✖' if s.is_booked else '◯'}]" for s in row.seats]
            row_str += " ".join(seat_visuals) + f" (Available: {row.available_seats_count})"
            print(row_str)
        print("---------------------------------\n")


# --- SIMULATION CONFIGURATION RUNNER ---
if __name__ == "__main__":
    # Create a small airplane cabin layout: 5 Rows, 6 Seats per row (A, B, C, D, E, F)
    engine = FlightSeatingEngine(num_rows=5, seats_per_row=6)
    engine.display_cabin_map()

    # 1. Family of 3 arrives
    engine.allocate_contiguous(3)
    
    # 2. Break up continuity by manually booking a random center seat in Row 2
    # This books seat 2D (Row 2, Column index 3)
    engine.rows[1].seats[3].is_booked = True
    engine.rows[1].available_seats_count -= 1
    print("📢 [SYSTEM NOTE] Seat 2D has been manually reserved for an individual passenger.")
    engine.display_cabin_map()

    # 3. Large family of 4 arrives! Row 1 has 3 seats left, Row 2 has 4 seats left but broken sequence
    engine.allocate_contiguous(4)
    
    engine.display_cabin_map()