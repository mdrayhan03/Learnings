from abc import ABC, abstractmethod

# Component
class FileSystemComponent(ABC) :
    @abstractmethod
    def display(self, indent=0) : pass

# Leaf  
class File(FileSystemComponent) :
    def __init__(self, name) :
        self.name = name

    def display(self, indent=0):
        print(f"{' ' * indent}File: {self.name}")

# Composite
class Folder(FileSystemComponent) :
    def __init__(self, name) :
        self.name = name
        self.contents = []

    def add(self, content: FileSystemComponent) :
        self.contents.append(content)

    def display(self, indent=0):
        print(f"{' ' * indent}Folder: {self.name}")

        for item in self.contents :
            item.display(indent + 2)


# --- Test it out ---
root = Folder("Root")
docs = Folder("Documents")
pic = File("cat.jpg")

docs.add(File("resume.pdf"))
root.add(docs)
root.add(pic)

# This should print the whole tree recursively
root.display()