from abc import ABC, abstractmethod

class Bird(ABC) :
    @abstractmethod
    def walk(self) : pass

class FlyingBird(Bird, ABC) :
    @abstractmethod
    def fly(self) : pass
        

class Eagle(FlyingBird) :
    def walk(self):
        return "I am walking!"
    
    def fly(self):
        return "I am flying high!"

class NonFlyingBird(Bird, ABC) :
    pass

class Ostrich(NonFlyingBird) :
    def walk(self):
        return "I am walking!"

def make_bird_fly(bird: FlyingBird):
    print(bird.fly())

make_bird_fly(Eagle())    # Works perfectly
make_bird_fly(Ostrich())  # BOOM! Crashes the program.