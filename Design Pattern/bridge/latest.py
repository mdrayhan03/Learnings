from abc import ABC, abstractmethod

class MessagingChannel(ABC):
    @abstractmethod
    def send_data(self, data): pass

class EmailChannel(MessagingChannel):
    def send_data(self, data):
        return f"Sending Email: {data}"

class SMSChannel(MessagingChannel):
    def send_data(self, data):
        return f"Sending SMS: {data}"
    
class PushChannel(MessagingChannel):
    def send_data(self, data):
        return f"Sending Push: {data}"
    

class Notification(ABC):
    def __init__(self, channel: MessagingChannel):
        self.channel = channel

    @abstractmethod
    def announce(self, message): pass

# 3. Refined Abstractions
class UrgentNotification(Notification):
    def announce(self, message):
        formatted = f"!!! PRIORITY !!! {message}"
        return self.channel.send_data(formatted)

class NormalNotification(Notification):
    def announce(self, message):
        return self.channel.send_data(message)

# What happens if we add 'PushNotification'? 
# We'd have to create 'UrgentPush' and 'NormalPush'.
# What if we add 'SecretMessage'? 
# We'd need 'SecretEmail', 'SecretSMS', and 'SecretPush'.

# Execution
# 4. Execution - Any Notification can work with Any Channel
email = EmailChannel()
sms = SMSChannel()
push = PushChannel()

# Mix and match!
msg1 = UrgentNotification(email)
print(msg1.announce("Server Down!"))

msg2 = NormalNotification(sms)
print(msg2.announce("Order Shipped."))

msg3 = UrgentNotification(push)
print(msg3.announce("New offer."))