class Event :
    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload

class SimpleMessageBroker :
    def __init__(self):
        self.event_bindings = {}
        self.queues = {}
        self.active_consumers = {}

    def register_queue(self, queue_name: str, event_name: str) :
        if queue_name not in self.queues :
            self.queues[queue_name] = []
        
        # Connect the event name to this queue
        if event_name not in self.event_bindings:
            self.event_bindings[event_name] = []
            
        if queue_name not in self.event_bindings[event_name]:
            self.event_bindings[event_name].append(queue_name)
            
        print(f"[BROKER] Permanent queue '{queue_name}' is now BOUND to event '{event_name}'")

    def connect_consumer(self, queue_name: str, callback_function) :
        self.active_consumers[queue_name] = callback_function
        print(f"[BROKER] Service bound to '{queue_name}' successfully.")
        
        # Drain any messages that piled up while the service was dead!
        self._flush_queue(queue_name)

    def disconnect_consumer(self, queue_name: str) :
        if queue_name in self.active_consumers:
            del self.active_consumers[queue_name]
            print(f"[BROKER] ALERT: '{queue_name}' disconnected! (Simulating crash/restart)")

    def publish(self, event: Event):
        """
        NOW CONNECTED: Looks up all queues bound to this event name, 
        drops a copy of the message in each, and flushes online queues.
        """
        event_name = event.name
        print(f"\n[BROKER] Received published event: '{event_name}'")

        # Check if any queues are bound to this specific event name
        if event_name not in self.event_bindings or not self.event_bindings[event_name]:
            print(f"[BROKER] No queues are listening for event '{event_name}'. Dropping message.")
            return

        # Loop through every queue box that is registered to this event
        for queue_name in self.event_bindings[event_name]:
            # Route a copy of the payload to this queue's storage box
            self.queues[queue_name].append(event.payload)
            print(f"[BROKER] Routed message copy to queue storage: '{queue_name}'")
            
            # If this specific queue has an active consumer online, deliver immediately
            if queue_name in self.active_consumers:
                self._flush_queue(queue_name)
            else:
                print(f"[BROKER] Queue '{queue_name}' is currently OFFLINE. Saving message safely...")

    def _flush_queue(self, queue_name: str):
        """Safely drains stacked messages out of a box to an active consumer."""
        callback = self.active_consumers[queue_name]
        while self.queues[queue_name]:
            msg_payload = self.queues[queue_name].pop(0)
            callback(msg_payload)

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

    broker.register_queue("email-service-queue", "OrderPlaced")
    broker.register_queue("inventory-service-queue", "OrderPlaced")

    print("\n--- 2. Initializing Core Microservices ---")
    order_service = OrderService(broker)
    inventory_service = InventoryService(broker)
    email_service = EmailNotificationService(broker)

    print("\n--- 3. Subscribing Services to the Event Stream ---")
    # Registering the consumer callbacks with the broker
    broker.connect_consumer("inventory-service-queue", inventory_service.on_order_place)
    broker.connect_consumer("email-service-queue", email_service.send_confirmation)

    print("\n--- 4. Simulating Live Traffic ---")
    # Triggering the event pipeline
    order_service.place_order(order_id=9001, item="MacBook Pro")
    order_service.place_order(order_id=9002, item="Wireless Headphones")