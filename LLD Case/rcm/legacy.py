import threading
import time
import random

class UnsafeShowSeat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.is_booked = False
        self.booked_by = None

class UnsafeBookingEngine:
    def __init__(self):
        self.seat = UnsafeShowSeat("VIP-RowA-Seat1")
        self.successful_bookings_count = 0
        self._lock = threading.RLock()

    def attempt_booking(self, user_id):
        # ⚠️ CRITICAL SECTION - Completely Unprotected!
        with self._lock :
            if not self.seat.is_booked:
                # Introduce a tiny sleep to simulate database IO latency
                # This dramatically amplifies the race condition window
                time.sleep(random.uniform(0.001, 0.005))
                
                self.seat.is_booked = True
                self.seat.booked_by = user_id
                self.successful_bookings_count += 1
                print(f"🎉 [SUCCESS] User {user_id} successfully booked seat {self.seat.seat_id}!")
                return True
        return False

# --- Simulation Setup ---
engine = UnsafeBookingEngine()
threads = []

# Spawn 1,000 threads executing at the exact same time
for i in range(1, 1001):
    t = threading.Thread(target=engine.attempt_booking, args=(f"User-{i}",))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"\n💥 Total Successful Booking Counts Claimed: {engine.successful_bookings_count}")
# A safe engine must print EXACTLY 1. This unsafe version will print a much higher number!