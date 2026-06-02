from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC) :
    @abstractmethod
    def eat_lunch(self): pass

class HumanWorker(Worker, Eatable):
    def work(self):
        return "Human typing code..."
        
    def eat_lunch(self):
        return "Eating a sandwich..."

class RobotWorker(Worker):
    def work(self):
        return "Robot assembling parts..."