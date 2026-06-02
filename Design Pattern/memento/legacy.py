class TextEditor:
    def __init__(self):
        self.content = ""
        # PROBLEM 1: The editor is managing its own history (violates Single Responsibility)
        self.history = [] 

    def write(self, new_text):
        # PROBLEM 2: We are saving the state manually every time.
        # What if we only want to save at specific checkpoints?
        self.history.append(self.content) 
        self.content += new_text

    def undo(self):
        if self.history:
            # PROBLEM 3: Logic is tightly coupled to the list structure.
            self.content = self.history.pop()
        else:
            print("Nothing to undo!")

# Execution
editor = TextEditor()
editor.write("Hello ")
editor.write("World!")
print(f"Current: {editor.content}")

editor.undo()
print(f"After Undo: {editor.content}")

# PROBLEM 4: Direct Access. 
# Anyone can reach in and mess with the history because it's just a public list.
editor.history.clear()