import threading
import time
import random

class DeadlockProneAccount:
    def __init__(self, account_id: str, initial_balance: float):
        self.account_id = account_id
        self.balance = initial_balance
        self._lock = threading.Lock() # Individual account lock wrapper

class NaiveBankEngine:
    def transfer_funds(self, from_acc: DeadlockProneAccount, to_acc: DeadlockProneAccount, amount: float):
        print(f"💸 [START] Thread {threading.current_thread().name} initiating transfer from {from_acc.account_id} -> {to_acc.account_id}")
        
        # ⚠️ CRITICAL FLAW: Acquiring locks based on arrival positioning!
        with from_acc._lock:
            print(f"🔒 [LOCKED] Thread {threading.current_thread().name} secured {from_acc.account_id}")
            
            # Artificial sleep window to amplify the deadlock arrival overlap
            time.sleep(0.01)
            
            print(f"⏳ [WAITING] Thread {threading.current_thread().name} trying to grab lock for {to_acc.account_id}...")
            with to_acc._lock:
                if from_acc.balance >= amount:
                    from_acc.balance -= amount
                    to_acc.balance += amount
                    print(f"✅ [SUCCESS] Transfer complete! {amount} moved.")
                else:
                    print("❌ [FAILED] Insufficient balance.")

# --- Simulation Configuration Setup ---
acc_A = DeadlockProneAccount("ACC-1111", 500.0)
acc_B = DeadlockProneAccount("ACC-9999", 500.0)
engine = NaiveBankEngine()

# Thread 1: Moves funds from A to B
t1 = threading.Thread(target=engine.transfer_funds, args=(acc_A, acc_B, 50.0), name="Transfer-A-To-B")
# Thread 2: Moves funds from B to A at the exact same millisecond
t2 = threading.Thread(target=engine.transfer_funds, args=(acc_B, acc_A, 100.0), name="Transfer-B-To-A")

print("--- Launching Cyclic Concurrent Bank Transfer Pipeline ---")
t1.start()
t2.start()

t1.join()
t2.join()
print("🏁 Engine Finished Processed Successfully!") # ⚠️ This print line will never be reached!