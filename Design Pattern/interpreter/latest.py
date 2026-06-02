from abc import ABC, abstractmethod

class Expression(ABC) :
    @abstractmethod
    def interpret(self, context) : pass

class MoveUpExpression(Expression) :
    def interpret(self, context):
        context.y += 1

class MoveDownExpression(Expression) :
    def interpret(self, context):
        context.y -= 1

class MoveLeftExpression(Expression) :
    def interpret(self, context):
        context.x -= 1

class MoveRightExpression(Expression) :
    def interpret(self, context):
        context.x += 1

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"Robot is at ({self.x}, {self.y})"

class RobotParser:
    @staticmethod
    def parse(command_string) :
        tree = []
        tokens = command_string.split(" ")

        mapping = {
            "up" : MoveUpExpression(),
            "down":  MoveDownExpression(),
            "left" : MoveLeftExpression(),
            "right" : MoveRightExpression(),
        }

        for token in tokens :
            if token in mapping :
                tree.append(mapping[token])

        return tree
    
bot = Robot()
commands = "up up right"

instructions = RobotParser.parse(commands)

for exprssion in instructions :
    exprssion.interpret(bot)

print(bot)