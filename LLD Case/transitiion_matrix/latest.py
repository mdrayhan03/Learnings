import threading
import time

class MatrixVendingMachine:
    # 1. Define your States as clean constants
    STATE_IDLE = "IDLE"
    STATE_HAS_MONEY = "HAS_MONEY"
    STATE_DISPENSING = "DISPENSING"
    STATE_OUT_OF_STOCK = "OUT_OF_STOCK"

    # 2. Define your Events as clean constants
    EVENT_INSERT_MONEY = "INSERT_MONEY"
    EVENT_SELECT_PRODUCT = "SELECT_PRODUCT"
    EVENT_DISPENSE = "DISPENSE"
    EVENT_CANCEL = "CANCEL"

    def __init__(self):
        self._current_state = self.STATE_IDLE
        self._lock = threading.RLock() # Keeps our matrix thread-safe
        
        self.inventory = {1: {"name": "soda", "stock": 1}}
        self.selected_product = None

        # 3. THE MATRIX: State + Event = Next State
        # If a combination isn't listed here, it is automatically an invalid action!
        self._transition_matrix = {
            self.STATE_IDLE: {
                self.EVENT_INSERT_MONEY: self.STATE_HAS_MONEY
            },
            self.STATE_HAS_MONEY: {
                self.EVENT_INSERT_MONEY: self.STATE_HAS_MONEY, # Additional money accepted
                self.EVENT_SELECT_PRODUCT: self.STATE_DISPENSING, # Dynamic check happens in action
                self.EVENT_CANCEL: self.STATE_IDLE
            },
            self.STATE_DISPENSING: {
                # Dispensing blocks outside events. Transitions are driven internally by results!
            },
            self.STATE_OUT_OF_STOCK: {
                self.EVENT_INSERT_MONEY: self.STATE_HAS_MONEY,
                self.EVENT_CANCEL: self.STATE_IDLE
            }
        }

    # 4. THE TRAFFIC CONTROLLER: The central handle_event function
    def handle_event(self, event: str, payload=None):
        with self._lock:
            # Step A: Look up the next state in the matrix in O(1) time
            allowed_transitions = self._transition_matrix.get(self._current_state, {})
            next_state = allowed_transitions.get(event)

            # Special case for internal dispatching logic
            if self._current_state == self.STATE_DISPENSING and event == self.EVENT_DISPENSE:
                self._execute_action(event, payload)
                return

            # Step B: If the lookup fails, block the operation immediately
            if not next_state:
                print(f"❌ [ERROR] Action '{event}' is denied while machine is in '{self._current_state}' state.")
                return

            # Step C: Transition state and execute internal code
            print(f"🔄 [TRANSITION] State moving from {self._current_state} ──({event})──> {next_state}")
            self._current_state = next_state
            self._execute_action(event, payload)

    # 5. THE ACTION ROUTER: Executes business logic associated with the event
    def _execute_action(self, event, payload):
        if event == self.EVENT_INSERT_MONEY:
            print(f"💵 Money updated! Received: ${payload}")
            
        elif event == self.EVENT_SELECT_PRODUCT:
            product_id = payload
            product = self.inventory.get(product_id)
            
            if not product or product.get("stock") == 0:
                print(f"⚠️ Selected item is out of stock! Rediverting to out of stock status.")
                self._current_state = self.STATE_OUT_OF_STOCK
            else:
                print(f"🎯 Selected {product.get('name')}. Initializing dispatch sequence...")
                self.selected_product = product
                # Automatically trigger the internal dispense loop!
                self.handle_event(self.EVENT_DISPENSE)
                
        elif event == self.EVENT_DISPENSE:
            product = self.selected_product
            time.sleep(0.5) # Artificial race condition latency simulation
            
            if product.get("stock") <= 0:
                print(f"🚨 Race failure: Item emptied mid-air!")
                self._current_state = self.STATE_OUT_OF_STOCK
            else:
                product["stock"] -= 1
                print(f"🥤 Released: {product.get('name')} issued. Remaining stock: {product['stock']}")
                self.selected_product = None
                
                # Check where to route the next state based on final stock values
                if product.get("stock") == 0:
                    self._current_state = self.STATE_OUT_OF_STOCK
                else:
                    self._current_state = self.STATE_IDLE
            print(f"🏁 [SYSTEM STATUS] Machine is now safely back in state: {self._current_state}")
                    
        elif event == self.EVENT_CANCEL:
            print("🛑 Transaction canceled. Refunding deposits.")

# ==========================================
# CONCURRENT MATRIX TESTING ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    vm = MatrixVendingMachine()

    # Client code doesn't call custom methods. It just sends events down the pipeline!
    vm.handle_event(vm.EVENT_INSERT_MONEY, payload=5)
    
    # We trigger product selection, which internally forwards directly into Dispensing
    # We simulate simultaneous multi-threaded execution triggers
    thread1 = threading.Thread(target=vm.handle_event, args=(vm.EVENT_SELECT_PRODUCT, 1))
    thread2 = threading.Thread(target=vm.handle_event, args=(vm.EVENT_SELECT_PRODUCT, 1))

    print("\n--- Executing Concurrent Matrix Thread Attacks ---")
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    # Check to see if illegal actions are successfully caught at the front gate
    vm.handle_event(vm.EVENT_CANCEL)