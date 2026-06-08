from abc import ABC, abstractmethod

# outbound port
class Repository(ABC) : pass

class AlertRepository(Repository) :
    @abstractmethod
    def save_alert_log(self, log): pass

class NotifierRepository(Repository) :
    @abstractmethod
    def send_urgent_alert(self, message) : pass

# outside tools
class InMemoryAlertAdapter(AlertRepository) :
    def save_alert_log(self, log):
        print(f"[IN Memory] {log}")
    
class FileAlertAdapter(AlertRepository) :
    def save_alert_log(self, log):
        print(f"[File] {log}")
    
class ConsoleNotificationAdapter(NotifierRepository) :
    def send_urgent_alert(self, message):
        print(f"[Console] URGENT:{message}")
    
class SMSNotificationAdapter(NotifierRepository) :
    def send_urgent_alert(self, message):
        print(f"[SMS] URGENT: {message}")

class StockService :
    def __init__(self, alert_repo: AlertRepository, notify_repo: NotifierRepository):
        self.alert_repo = alert_repo
        self.notify_repo = notify_repo

    def check_stock_level(self, product_name, current_stock, threshold) :
        if current_stock < threshold :
            message = f"Product Name: {product_name}\nCurrent Stock: {current_stock}\nGOES DOWN THRESHOLD {threshold}."

            self.alert_repo.save_alert_log(message)
            self.notify_repo.send_urgent_alert(message)

if __name__ == "__main__" :
    alert_repo = InMemoryAlertAdapter()
    notify_repo = ConsoleNotificationAdapter()

    stock_service = StockService(alert_repo, notify_repo)

    stock_service.check_stock_level("Product 1", 10, 11)