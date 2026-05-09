class File:
    def __init__(self, name):
        self.name = name
    def display(self):
        print(f"File: {self.name}")

class Folder:
    def __init__(self, name):
        self.name = name
        self.contents = []
    def add(self, item):
        self.contents.append(item)
    # The mess: We have to manually loop and check if it's a file or folder
    def show_folder_contents(self):
        print(f"Folder: {self.name}")
        for item in self.contents:
            item.display() # Only works if everything has .display()


root = Folder("Root")
docs = Folder("Documents")
pic = File("cat.jpg")

docs.add(File("resume.pdf"))
root.add(docs)
root.add(pic)

# This should print the whole tree recursively
root.show_folder_contents()