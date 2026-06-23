class NaiveSeat:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_booked = False

class NaiveFlightEngine:
    def __init__(self, total_rows, seats_per_row):
        # Generates a basic raw nested grid array
        self.grid = [[NaiveSeat(r, c) for c in range(seats_per_row)] for r in range(total_rows)]

    def book_contiguous_seats(self, num_seats):
        # ⚠️ Clunky, error-prone index jumping to find consecutive slots
        for r in range(len(self.grid)):
            consecutive_count = 0
            start_col = -1
            
            for c in range(len(self.grid[r])):
                if not self.grid[r][c].is_booked:
                    if consecutive_count == 0:
                        start_col = c
                    consecutive_count += 1
                    
                    if consecutive_count == num_seats:
                        # Found it! Now loop back to book them
                        for i in range(start_col, start_col + num_seats):
                            self.grid[r][i].is_booked = True
                        print(f"Booked {num_seats} seats in Row {r} starting from Col {start_col}")
                        return True
                else:
                    consecutive_count = 0  # Broken sequence, reset completely
        print("No matching consecutive blocks found!")
        return False