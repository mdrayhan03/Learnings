class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def execute_commands(self, command_string):
        # PROBLEM: This is hardcoded logic. 
        # If we add "jump" or "multiply", this loop becomes a nightmare.
        # It doesn't support complex grammar like "move(up, 5)"
        commands = command_string.split(" ")
        for cmd in commands:
            if cmd == "up":
                self.y += 1
            elif cmd == "down":
                self.y -= 1
            elif cmd == "left":
                self.x -= 1
            elif cmd == "right":
                self.x += 1
        
        print(f"Robot is at ({self.x}, {self.y})")

# Usage
bot = Robot()
bot.execute_commands("up up right")