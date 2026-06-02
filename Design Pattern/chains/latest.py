from abc import ABC, abstractmethod

class Handler(ABC) :
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler) :
        self._next_handler = handler 
        return handler

    @abstractmethod
    def handle(self, issue_type, severity) : 
        if self._next_handler:
            return self._next_handler.handle(issue_type, severity)
        print("System: No one could handle this request. Dropped.")

class BillingHandler(Handler) :
    def handle(self, issue_type, severity):
        if issue_type == "billing" :
            print(f"Billing Dept: Processing payment issue with severity {severity}.")
        
        else :
            super().handle(issue_type, severity)

class TechnicalHandler(Handler) :
    def handle(self, issue_type, severity):
        if issue_type == "technical" :
            if severity == "critical" :
                print(f"Senior Engineer: Fixing critical server failure!")
            else:
                print(f"Junior Tech: Fixing minor technical glitch.")
        else :
            super().handle(issue_type, severity)

class GeneralHandler(Handler) :
    def handle(self, issue_type, severity):
        if issue_type == "general" :
            print(f"Bot: Automated response sent for general inquiry.")
        else :
            super().handle(issue_type, severity)

class HandlerManager :
    def __init__(self, first_handler):
        self._first_handler = first_handler

    def get_first_handler(self) :
        return self._first_handler
    
    def handle(self, issue_type, severity) :
        self._first_handler.handle(issue_type, severity)

manager = HandlerManager(BillingHandler())

manager.get_first_handler().set_next(TechnicalHandler()).set_next(GeneralHandler())

# --- Usage ---
print("--- Request 1 ---")
manager.handle("technical", "critical")

print("\n--- Request 2 ---")
manager.handle("billing", "low")

print("\n--- Request 3 ---")
manager.handle("unknown", "none")