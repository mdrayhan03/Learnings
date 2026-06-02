class Bird:
    def fly(self):
        return "I am flying high!"

class Eagle(Bird):
    pass

class Ostrich(Bird):
    def fly(self):
        # PROBLEM: An Ostrich cannot fly! 
        # Forcing it to inherit fly() breaks the application's expectations
        # if a loop is processing all "Birds" and assuming they can fly.
        raise NotImplementedError("Ostriches can't fly!")

# A client function that expects ANY bird to fly safely
def make_bird_fly(bird: Bird):
    print(bird.fly())

make_bird_fly(Eagle())    # Works perfectly
make_bird_fly(Ostrich())  # BOOM! Crashes the program.