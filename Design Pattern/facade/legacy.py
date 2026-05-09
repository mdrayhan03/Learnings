class Amplifier:
    def turn_on(self): print("Amp: On")
    def set_volume(self, level): print(f"Amp: Volume set to {level}")

class Projector:
    def turn_on(self): print("Projector: On")
    def set_input(self, device): print(f"Projector: Input set to {device}")

class Lights:
    def dim(self, level): print(f"Lights: Dimmed to {level}%")

class DVDPlayer:
    def turn_on(self): print("DVD: On")
    def play(self, movie): print(f"DVD: Playing '{movie}'")

# --- The Messy Client ---
# The user has to know how to talk to 4 different classes just to watch a movie!
amp = Amplifier()
proj = Projector()
light = Lights()
dvd = DVDPlayer()

light.dim(10)
amp.turn_on()
amp.set_volume(20)
proj.turn_on()
proj.set_input("DVD")
dvd.turn_on()
dvd.play("Inception")