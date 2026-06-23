import threading
import time
import random
import queue  # Core thread-safe Blocking FIFO Queue

class ShowSeat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.is_booked = False
        self.booked_by = None


class ShowSeatRepository:
    def __init__(self):
        self.seats = []
    
    def add_seat(self, seat: ShowSeat):
        self.seats.append(seat)
    
    def get_seat(self, seat_id):
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat
        return None
    
    def print_seats(self):
        print("\n--- Final Seat Layout Map State ---")
        for idx, seat in enumerate(self.seats):
            status = "◯" if not seat.is_booked else f"✖ (User: {seat.booked_by})"
            print(f"[{seat.seat_id}:{status}]", end="   ")
            if (idx + 1) % 4 == 0:
                print()
        print("\n------------------------------------")


class PaymentConnectionPool:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self._pool = [f"Conn-Socket-{i}" for i in range(1, max_capacity + 1)]
        
        # Primitive A: Semaphore manages capacity throttling boundaries
        self._semaphore = threading.Semaphore(max_capacity)
        # Primitive B: Standard Mutex protects list data integrity from overlapping mutations
        self._list_lock = threading.Lock()

    def get_connection(self, worker_id: str) -> str:
        self._semaphore.acquire()
        with self._list_lock:
            connection = self._pool.pop(0)
            print(f"🔌 [POOL CHECKOUT] {worker_id} acquired {connection}. Available Slots: {len(self._pool)}")
        return connection

    def release_connection(self, connection: str, worker_id: str):
        with self._list_lock:
            self._pool.append(connection)
            print(f"♻️ [POOL RETURN]   {worker_id} returned {connection}. Available Slots: {len(self._pool)}")
        self._semaphore.release()


class PullPaymentEngine:
    def __init__(self, payment_pool: PaymentConnectionPool):
        self.payment_pool = payment_pool
        # The central coordination boundary where tasks accumulate safely
        self.waiting_queue = queue.Queue()

    def add_payment_to_queue(self, seat: ShowSeat):
        """Called by Producers to safely buffer new requests"""
        print(f"📥 [QUEUE ADD] Seat {seat.seat_id} buffered into task channel.")
        self.waiting_queue.put(seat)

    def start_worker_pool(self, num_workers=3):
        """
        🎯 THE PULL PATTERN INITIALIZATION:
        Spawns a fixed collection of long-lived peer threads. They stay alive 
        permanently, pulling work items from the queue whenever they clear out.
        """
        print(f"🛠️  [SYSTEM] Initializing {num_workers} Pull-Based Concurrent Background Workers...")
        for i in range(1, num_workers + 1):
            t = threading.Thread(
                target=self._worker_loop, 
                args=(f"PullWorker-{i}",), 
                daemon=True
            )
            t.start()

    def _worker_loop(self, thread_name: str):
        """The permanent infinite loop running inside each pool worker"""
        while True:
            # 🛑 BLOCKED POINT (SLEEP): Python's queue engine safely handles the thread locks.
            # If the queue is empty, the thread goes to sleep automatically.
            # When an item is added, the queue awakens EXACTLY ONE worker.
            seat = self.waiting_queue.get()
            
            print(f"💳 [⚡ PULL PROCESSING] {thread_name} pulled seat {seat.seat_id} from queue.")
            
            # Fetch connection from our throttling pool
            connection = self.payment_pool.get_connection(seat.booked_by)
            
            # Simulate real network payment gateway round-trip processing time
            time.sleep(random.uniform(0.2, 0.4))
            
            print(f"✅ [⚡ PULL SUCCESS] {thread_name} finalized transaction for seat {seat.seat_id}!")
            self.payment_pool.release_connection(connection, seat.booked_by)
            
            # Inform the queue architecture that a processing cycle unit has completed
            self.waiting_queue.task_done()


class BookingEngine:
    def __init__(self, seat_repo: ShowSeatRepository, payment_engine: PullPaymentEngine):
        self.seat_repo = seat_repo
        self.payment_engine = payment_engine
        self.successful_bookings_count = 0
        self._lock = threading.RLock() # Reentrant lock avoids internal deadlock cascades

    def attempt_booking(self, user_id, seat_id):
        # Critical Section isolation: Prevents concurrent race conditions on seat updates
        with self._lock:
            seat = self.seat_repo.get_seat(seat_id)
            if seat and not seat.is_booked:
                time.sleep(random.uniform(0.001, 0.005)) # Simulated system write lag
                
                seat.is_booked = True
                seat.booked_by = user_id
                self.successful_bookings_count += 1
                print(f"🎉 [BOOKING RECONCILED] User {user_id} secured seat {seat.seat_id}!")
                
                # Asynchronous Hand-off: Toss onto queue, then instantly exit lock
                self.payment_engine.add_payment_to_queue(seat)
                return True
        return False


# --- RUNNER LAYOUT SIMULATION ---
if __name__ == "__main__":
    # 1. Setup seed inventories
    seat_repository = ShowSeatRepository()
    for seat_lbl in ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]:
        seat_repository.add_seat(ShowSeat(seat_lbl))
    
    # 2. Limit our infrastructure down to 3 database slots
    connection_pool = PaymentConnectionPool(max_capacity=3)
    
    # 3. Create our Pull engine and spin up 3 background listeners
    pay_engine = PullPaymentEngine(payment_pool=connection_pool)
    pay_engine.start_worker_pool(num_workers=3)
    
    # 4. Initialize core allocation router
    booking_engine = BookingEngine(seat_repo=seat_repository, payment_engine=pay_engine)

    # 5. Launch 100 threads colliding on the same row segment coordinates simultaneously
    threads = []
    print("\n--- Initiating High-Scale Pull-Model Queue Engine Execution ---")
    
    for i in range(1, 101):
        target_seat_id = f"A{random.randint(1, 7)}"
        t = threading.Thread(
            target=booking_engine.attempt_booking, 
            args=(f"User-{i}", target_seat_id)
        )
        threads.append(t)
        t.start()

    # Block main thread execution until booking contention finishes
    for t in threads:
        t.join()

    # Block main program lifecycle until the concurrent worker threads drain the queue entirely
    pay_engine.waiting_queue.join()

    print("\n🔒 Final Operational Audit Report Verification:")
    print(f"🛡️ Total Reconciled Records: {booking_engine.successful_bookings_count} / 4 total physical spots.")
    
    seat_repository.print_seats()