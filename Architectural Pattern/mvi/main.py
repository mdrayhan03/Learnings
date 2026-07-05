from abc import ABC, abstractmethod

#############
# M -> Immutable State Snapshot (Model Context)
#############
class CounterState:
    def __init__(self, count: int, error_message: str | None = None):
        # Enforcing immutability by convention (fields are evaluated as read-only snapshots)
        self.count: int = count
        self.error_message: str | None = error_message

#############
# I -> Intent (User Actions)
#############
class Intent(ABC): pass

class IncrementIntent(Intent): pass
class DecrementIntent(Intent): pass
class ResetIntent(Intent): pass

#############
# S -> The State Store / Processor
#############
class CounterStore:
    def __init__(self):
        # Single Source of Truth initialized as a clean state snapshot
        self._current_state: CounterState = CounterState(count=0, error_message=None)
        self.on_state_changed = None

    def dispatch(self, intent: Intent) -> None:
        """
        The central reduction engine. Evaluates incoming intents, reads the 
        current state, and emits a brand-new state snapshot.
        """
        current_count = self._current_state.count
        new_count = current_count
        new_error = None

        # Reducer state machine calculations
        if isinstance(intent, IncrementIntent):
            new_count = current_count + 1
            
        elif isinstance(intent, DecrementIntent):
            # Enforce a strict boundary rule constraint
            if current_count <= 0:
                new_error = "Operation Denied: Count cannot fall below 0!"
            else:
                new_count = current_count - 1
                
        elif isinstance(intent, ResetIntent):
            new_count = 0

        # UNIDIRECTIONAL LOOP STEP: Create a completely NEW state instance (No mutation!)
        self._current_state = CounterState(count=new_count, error_message=new_error)

        # Broadcast the state snapshot out to all subscribed view views
        if self.on_state_changed:
            self.on_state_changed(self._current_state)

############
# V -> Pure State View
############
class CounterView:
    def __init__(self, counter_store: CounterStore):
        self._store: CounterStore = counter_store
        # Wire up the state stream hook to our pure layout renderer
        self._store.on_state_changed = self.render

    def render(self, state: CounterState) -> None:
        """
        A completely pure function of state. It clears out old context and
        constructs the UI strictly from the fields inside the snapshot.
        """
        print("\n" + "—" * 40)
        print("            COUNTER DEVICE SCREEN")
        print("—" * 40)
        print(f"  Current Digital Tally Display: [ {state.count} ]")
        
        if state.error_message:
            print(f"  ⚠️ ALERT REGISTERED: {state.error_message}")
        print("—" * 40)

#############
# Simulation
#############
if __name__ == "__main__":
    print("--- 1. Initializing Unidirectional MVI Machine ---")
    store = CounterStore()
    view = CounterView(store)
    
    # Display the initial screen manually to kick off layout context
    view.render(store._current_state)

    # -----------------------------------------------------------------
    # SIMULATION: Simulating user click triggers flowing into Intents
    # -----------------------------------------------------------------
    print("\n--- 2. User clicks the [+] Button twice ---")
    # View converts raw button events into declarative Intent objects
    store.dispatch(IncrementIntent())
    store.dispatch(IncrementIntent())

    print("\n--- 3. User clicks the [-] Button once ---")
    store.dispatch(DecrementIntent())

    print("\n--- 4. User clicks the [-] Button past the boundary ---")
    store.dispatch(DecrementIntent())
    store.dispatch(DecrementIntent())  # This one should hit our 0 limit check

    print("\n--- 5. User clicks the [Reset] Button ---")
    store.dispatch(ResetIntent())