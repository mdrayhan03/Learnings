import copy

class TextSave:
    def __init__(self, state):
        self._state = copy.deepcopy(state)

    def get_saved_state(self) :
        return self._state

class TextEditor :
    def __init__(self):
        self._content = ""

    def write(self, content) :
        self._content += ' '
        self._content += content
    
    def save(self) :
        return TextSave({"content": self._content})

    def restore(self, memento: TextSave) :
        state = memento.get_saved_state()
        self._content = state['content']

class TextHistoryManager :
    def __init__(self):
        self._history = []

    def backup(self, memento: TextSave) :
        self._history.append(memento)

    def undo(self) :
        if not self._history :
            return None
        return self._history.pop()
    
# execution
text_editor = TextEditor()
history_manager = TextHistoryManager()

text_editor.write("Hello ")
history_manager.backup(text_editor.save())
text_editor.write("World!")
# history_manager.backup(text_editor.save())
print(f"Current: {text_editor._content}")

save_text = history_manager.undo()
if save_text :
    text_editor.restore(save_text)

print(f"After Undo: {text_editor._content}")