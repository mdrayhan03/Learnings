class UrgentEmailNotification:
    def send(self, message):
        print(f"Sending URGENT Email: {message} [Applying High Priority Headers]")

class NormalEmailNotification:
    def send(self, message):
        print(f"Sending Normal Email: {message}")

class UrgentSMSNotification:
    def send(self, message):
        print(f"Sending URGENT SMS: {message} [Sending via Premium Route]")

class NormalSMSNotification:
    def send(self, message):
        print(f"Sending Normal SMS: {message}")

# What happens if we add 'PushNotification'? 
# We'd have to create 'UrgentPush' and 'NormalPush'.
# What if we add 'SecretMessage'? 
# We'd need 'SecretEmail', 'SecretSMS', and 'SecretPush'.

# Execution
notif1 = UrgentEmailNotification()
notif1.send("Server is down!")

notif2 = NormalSMSNotification()
notif2.send("Your order has shipped.")