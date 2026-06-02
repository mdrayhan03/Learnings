class Character:
    def move(self):
        return "Walking forward"

class Warrior(Character):
    def attack(self):
        return "Swinging a sword!"

# PROBLEM: What if we want a Warrior that can fly? 
# We have to create a FlyingWarrior subclass. What if we want a Mage that flies? 
# A FlyingMage subclass. This causes a massive "Class Explosion" nightmare.
class FlyingWarrior(Warrior):
    def move(self):
        return "Flying through the clouds!"