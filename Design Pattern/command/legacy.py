class Light:
    def turn_on(self): print("Light is ON")

class RemoteButton:
    def __init__(self, light):
        self.light = light

    def press(self):
        # Messy: The button is "married" to the Light. 
        # If I want it to open a Door, I have to change this class.
        self.light.turn_on()

light = Light()
remote = RemoteButton(light)

remote.press()