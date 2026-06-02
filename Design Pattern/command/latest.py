from abc import ABC, abstractmethod

class Command(ABC) :
    @abstractmethod
    def execute(self) :
        pass

    def undo(self) :
        pass

class Light:
    def turn_on(self): print("Light is ON")
    def turn_off(self): print("Light is OFF")

class LightOnCommand(Command) :
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self) :
        self.light.turn_off()

class Stereo:
    def turn_on(self): print("Stereo is ON")
    def turn_off(self): print("Stereo is OFF")

class StereoOnCommand(Command) :
    def __init__(self, stereo: Stereo):
        self.stereo = stereo
    
    def execute(self):
        self.stereo.turn_on()
    
    def undo(self) :
        self.stereo.turn_off()

class RemoteControl :
    def __init__(self):
        self._command: Command = None

    def set_command(self, command: Command) :
        self._command = command

    def press_button(self) :
        self._command.execute()
    
    def press_undo(self) :
        self._command.undo()

light = Light()
light_on = LightOnCommand(light)

stereo = Stereo()
stereo_on = StereoOnCommand(stereo)

remote = RemoteControl()
remote.set_command(light_on)
remote.press_button() # Light turns on
remote.press_undo()   # Light turns off!

remote.set_command(stereo_on)
remote.press_button() # stereo turns on
remote.press_undo()   # stereo turns off!