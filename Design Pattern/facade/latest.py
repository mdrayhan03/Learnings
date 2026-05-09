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
# amp = Amplifier()
# proj = Projector()
# light = Lights()
# dvd = DVDPlayer()

# light.dim(10)
# amp.turn_on()
# amp.set_volume(20)
# proj.turn_on()
# proj.set_input("DVD")
# dvd.turn_on()
# dvd.play("Inception")

class HomeTheaterFacade :
    def __init__(self, amp, light, proj, dvd):
        # We "inject" the existing devices into the facade
        self.amp = amp
        self.light = light
        self.proj = proj
        self.dvd = dvd

    def watch_movie(self, movie_title):
        print("\n--- Get ready for the show! ---")
        self.light.dim(10)
        self.amp.turn_on()
        self.amp.set_volume(20)
        self.proj.turn_on()
        self.proj.set_input("DVD")
        self.dvd.turn_on()
        self.dvd.play(movie_title)
        print("--- Enjoy! ---\n")

    def end_movie(self):
        print("\n--- Shutting everything down ---")
        self.light.dim(100)
        self.amp.turn_on() # or turn_off() if you have it
        self.dvd.turn_on()
        print("--- Goodbye ---\n")

# 1. Create the complex pieces once
my_amp = Amplifier()
my_light = Lights()
my_proj = Projector()
my_dvd = DVDPlayer()

# 2. Hand them to the Facade (The "Easy Button")
theater = HomeTheaterFacade(my_amp, my_light, my_proj, my_dvd)

# 3. Use one simple command
theater.watch_movie("Inception")