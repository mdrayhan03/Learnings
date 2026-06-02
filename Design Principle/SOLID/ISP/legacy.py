from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self): pass

    @abstractmethod
    def eat_lunch(self): pass

class HumanWorker(Worker):
    def work(self):
        return "Human typing code..."
        
    def eat_lunch(self):
        return "Eating a sandwich..."

class RobotWorker(Worker):
    def work(self):
        return "Robot assembling parts..."
        
    def eat_lunch(self):
        # PROBLEM: Robots don't eat! We are forcing this class 
        # to implement a useless method, violating ISP.
        pass