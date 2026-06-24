import threading
import time
import random

class BankAccount:
    def __init__(self, account_id: str, initial_balance: float):
        self.account_id = account_id
        self.balance = initial_balance
        self._lock = threading.Lock() # Individual localized lock object

class DeadlockFreeBankEngine:
    def transfer_funds(self, from_acc: BankAccount, to_acc: BankAccount, amount: float):
        print(f"💸 [START] Thread {threading.current_thread().name} initiating transfer from {from_acc.account_id} -> {to_acc.account_id}")
        
        # 🎯 THE FIX: STRICTOR GLOBAL RESOURCE ORDERING
        # Determine a deterministic lock acquisition sequence based on account IDs
        if from_acc.account_id < to_acc.account_id:
            first_lock_acc = from_acc
            second_lock_acc = to_acc
        else:
            first_lock_acc = to_acc
            second_lock_acc = from_acc

        print(f"⚖️ [SORTED] Thread {threading.current_thread().name} determined acquisition order: {first_lock_acc.account_id} then {second_lock_acc.account_id}")

        # 🔒 Step 1: Acquire the lowest id lock first
        with first_lock_acc._lock:
            print(f"🔒 [LOCKED-1] Thread {threading.current_thread().name} secured lock for {first_lock_acc.account_id}")
            
            # Artificial sleep window to prove that deadlocks are impossible
            time.sleep(0.02)
            
            print(f"⏳ [WAITING-2] Thread {threading.current_thread().name} trying to grab lock for {second_lock_acc.account_id}...")
            # 🔒 Step 2: Acquire the higher id lock second
            with second_lock_acc._lock:
                print(f"🔒 [LOCKED-2] Thread {threading.current_thread().name} secured lock for {second_lock_acc.account_id}")
                
                # Critical Section: Perform the ledger adjustments safely
                if from_acc.balance >= amount:
                    from_acc.balance -= amount
                    to_acc.balance += amount
                    print(f"✅ [SUCCESS] Thread {threading.current_thread().name} moved {amount} from {from_acc.account_id} -> {to_acc.account_id}")
                else:
                    print(f"❌ [FAILED] Thread {threading.current_thread().name} reported insufficient balance.")


# --- Simulation Configuration Setup ---
if __name__ == "__main__":
    # Create two accounts
    acc_A = BankAccount("ACC-1111", 500.0)
    acc_B = BankAccount("ACC-9999", 500.0)
    
    engine = DeadlockFreeBankEngine()

    # Thread 1: Moves funds from A to B (Tries to lock ACC-1111 then ACC-9999)
    t1 = threading.Thread(target=engine.transfer_funds, args=(acc_A, acc_B, 50.0), name="Tx-A-To-B")
    
    # Thread 2: Moves funds from B to A (ALSO tries to lock ACC-1111 then ACC-9999!)
    t2 = threading.Thread(target=engine.transfer_funds, args=(acc_B, acc_A, 100.0), name="Tx-B-To-A")

    print("--- Launching Deadlock-Free Concurrent Bank Transfer Pipeline ---")
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    print("\n🏁 Final Audit Balances Summary:")
    print(f"💰 {acc_A.account_id} Balance: ${acc_A.balance}")
    print(f"💰 {acc_B.account_id} Balance: ${acc_B.balance}")
    print("✅ Engine Finished Processing Successfully without freezing!")