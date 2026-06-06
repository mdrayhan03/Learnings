class Event :
    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload

class SimpleMessageBroker :
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name: str, callback_function) : 
        if event_name not in self.subscribers :
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback_function)
        print(f"[BROKER] New subscriber registered for event: '{event_name}'")

    def publish(self, event: Event) :
        event_name = event.name

        if event_name in self.subscribers :
            for callback in self.subscribers[event_name] :
                callback(event.payload)

class OrderService :
    def __init__(self, broker: SimpleMessageBroker):
        self.broker = broker

    def place_order(self, order_id, item) :
        print(f"\n[ORDER SERVICE] Processing order {order_id}...")
        
        # Instantiate the event object
        event = Event("OrderPlaced", {"order_id": order_id, "item": item})

        # Broadcast it to the broker
        self.broker.publish(event)
        print(f"[ORDER SERVICE] Broadcasted 'OrderPlaced' event for order {order_id}.")

class InventoryService :
    def __init__(self, broker: SimpleMessageBroker):
        self.broker = broker

    def on_order_place(self, payload) :
        print(f"[INVENTORY SERVICE] Deducting stock for item: '{payload.get('item')}' (Order ID: {payload.get('order_id')})")

class EmailNotificationService :
    def __init__(self, broker: SimpleMessageBroker):
        self.broker = broker

    def send_confirmation(self, payload) :
        print(f"[EMAIL SERVICE] Sending confirmation email for item: '{payload.get('item')}' (Order ID: {payload.get('order_id')})")

# =====================================================================
# EVENT ARCHITECTURE SIMULATION
# =====================================================================
if __name__ == "__main__":
    print("--- 1. Initializing Central Message Broker ---")
    broker = SimpleMessageBroker()

    print("\n--- 2. Initializing Core Microservices ---")
    order_service = OrderService(broker)
    inventory_service = InventoryService(broker)
    email_service = EmailNotificationService(broker)

    print("\n--- 3. Subscribing Services to the Event Stream ---")
    # Registering the consumer callbacks with the broker
    broker.subscribe("OrderPlaced", inventory_service.on_order_place)
    broker.subscribe("OrderPlaced", email_service.send_confirmation)

    print("\n--- 4. Simulating Live Traffic ---")
    # Triggering the event pipeline
    order_service.place_order(order_id=9001, item="MacBook Pro")
    order_service.place_order(order_id=9002, item="Wireless Headphones")