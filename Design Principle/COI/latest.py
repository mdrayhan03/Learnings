from abc import ABC, abstractmethod

class Behavior(ABC) :
    @abstractmethod
    def move(self): pass

class WalkBehavior(Behavior) :
    def move(self):
        return "Walking forward"
    
class FlyBehavior(Behavior) :
    def move(self):
        return "Flying through the clouds!"
    
class Character:
    def __init__(self, behavior: Behavior):
        self.behavior = behavior

class Warrior(Character):
    def attack(self):
        return "Swinging a sword!"
    
warrior = Warrior(WalkBehavior())
fly_warrior = Warrior(FlyBehavior())