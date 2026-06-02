from abc import ABC, abstractmethod

class Sender(ABC) :
    @abstractmethod
    def send(self, message) : pass

class EmailSender(Sender) :
    def send(self, message):
        print(f"Sending Email: {message}")

class NotificationManager :
    def __init__(self, sender: Sender):
        self.sender = sender
    
    def change_sender(self, sender: Sender) :
        self.sender = sender
    
    def send(self, msg) :
        self.sender.send(msg)

# Usage
sender = EmailSender()
notifier = NotificationManager()
notifier.set_sender(sender)
notifier.send("Hello World!")