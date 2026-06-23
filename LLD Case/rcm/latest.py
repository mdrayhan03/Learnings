import threading
import time
import random

class ThreadSafeShowSeat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.is_booked = False
        self.booked_by = None

class ThreadSafeBookingEngine:
    def __init__(self):
        self.seat = ThreadSafeShowSeat("VIP-RowA-Seat1")
        self.successful_bookings_count = 0
        self._lock = threading.RLock()  # Prevents self-deadlocks on nested execution pipelines

    def attempt_booking(self, user_id):
        with self._lock:
            if not self.seat.is_booked:
                # Simulated heavy database IO latency or network round-trips
                time.sleep(random.uniform(0.001, 0.005))
                
                self.seat.is_booked = True
                self.seat.booked_by = user_id
                self.successful_bookings_count += 1
                print(f"🎉 [SUCCESS] User {user_id} successfully booked seat {self.seat.seat_id}!")
                return True
        return False

# --- Simulation Setup ---
if __name__ == "__main__":
    engine = ThreadSafeBookingEngine()
    threads = []

    print("--- Simulating 1,000 Concurrent Booking Requests ---")

    for i in range(1, 1001):
        t = threading.Thread(target=engine.attempt_booking, args=(f"User-{i}",))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"\n🔒 Operational Safety Verification Audit:")
    print(f"🛡️ Total Successful Booking Counts Claimed: {engine.successful_bookings_count}")