import time

class GameCharacter:
    def __init__(self, name, role, health, weapon, spells):
        self.name = name
        self.role = role
        self.health = health
        self.weapon = weapon
        self.spells = spells
        # Simulate an "expensive" setup (e.g., loading textures/animations)
        print(f"--- Loading heavy assets for {self.name} ---")
        time.sleep(1) 

    def __str__(self):
        return f"{self.name} ({self.role}): HP {self.health}, Weapon: {self.weapon}"

# --- The Messy Way ---
# We have to re-define the whole "Orc" stats every time we want a new one
orc1 = GameCharacter("Orc Warrior", "Minion", 100, "Axe", ["Shout"])
orc2 = GameCharacter("Orc Warrior", "Minion", 100, "Axe", ["Shout"])
# orc3, orc4... it takes 1 second per orc!