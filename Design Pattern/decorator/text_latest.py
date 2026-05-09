from abc import ABC, abstractmethod

class Text() :
    def __init__(self, text):
        self.text = text
    
    def get_text(self) :
        return self.text

class TextDecorator(Text) :
    def __init__(self, text: Text):
        self._wrapper_text = text
    
    def get_text(self) :
        return self._wrapper_text.get_text()

class UnderlineDecorator(TextDecorator) :
    def get_text(self):
        return f"<u>{super().get_text()}</u>"
    
class BoldDecorator(TextDecorator) :
    def get_text(self):
        return f"<b>{super().get_text()}</b>"
    
text = UnderlineDecorator(Text("Hello world"))

print(text.get_text())