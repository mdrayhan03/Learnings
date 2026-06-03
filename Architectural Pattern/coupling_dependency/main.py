from abc import ABC, abstractmethod

class Channel(ABC) :
    def send(self, message) : pass

class EmailChannel(Channel) :
    def send(self, message):
        return f"Email: {message}"
    
class SMSChannel(Channel) :
    def send(self, message):
        return f"SMS: {message}"

class PushChannel(Channel) :
    def send(self, message):
        return f"Push: {message}"

class NotificationManager :
    def send_message(self, channel: Channel, message):
        print(channel.send(message))

