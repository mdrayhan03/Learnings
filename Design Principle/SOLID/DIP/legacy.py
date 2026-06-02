class EmailSender:
    def send_email(self, message):
        print(f"Sending Email: {message}")

class NotificationManager:
    def __init__(self):
        # PROBLEM: Hardcoded low-level module dependency!
        # This class controls the creation of its dependency.
        self.sender = EmailSender()

    def send(self, msg):
        self.sender.send_email(msg)

# Usage
notifier = NotificationManager()
notifier.send("Hello World!")