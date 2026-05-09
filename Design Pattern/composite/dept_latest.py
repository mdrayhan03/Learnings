from abc import ABC, abstractmethod

# Component
class OrganizationComponent(ABC) :
    @abstractmethod
    def get_salary(self) : pass

# Leaf
class Employee(OrganizationComponent) :
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_salary(self):
        print(f"Employee: {self.name}, Salary: {self.salary}tk")
        return self.salary
    
# Composite
class Department(OrganizationComponent) :
    def __init__(self, name):
        self.name = name
        self.contents = []

    def add(self, content: OrganizationComponent) :
        self.contents.append(content)

    def get_salary(self):
        cnt = 0
        print(f"Department: {self.name}")

        for employee in self.contents :
            cnt += employee.get_salary()
        
        print(f"Department: {self.name}, Total: {cnt}tk")
        return cnt
    
# Test code
dept1 = Department("Engineering")
emp1 = Employee("Rayhan", 25000)
emp2 = Employee("Ismile", 30000)

dept2 = Department("CSE")
emp3 = Employee("Sagor", 15000)

dept2.add(emp3)
dept1.add(emp1)
dept1.add(dept2)
dept1.add(emp2)

dept1.get_salary()