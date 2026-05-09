from abc import ABC, abstractmethod

class Button(ABC) :
    @abstractmethod
    def render(self) : pass

class LightButton(Button):
    def render(self): return "Rendering White Button"

class DarkButton(Button):
    def render(self): return "Rendering Charcoal Button"

class Checkbox(ABC):
    @abstractmethod
    def toggle(self): pass

class LightCheckbox:
    def toggle(self): return "Checking Light Box"

class DarkCheckbox:
    def toggle(self): return "Checking Dark Box"

class UIFactory(ABC) :
    @abstractmethod
    def create_button(self) -> Button : pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox : pass

class LightUIFactory(UIFactory) :
    def create_button(self):
        return LightButton()
    
    def create_checkbox(self):
        return LightCheckbox()
    
class DarkUIFactory(UIFactory) :
    def create_button(self):
        return DarkButton()
    
    def create_checkbox(self):
        return DarkCheckbox()

def client_code(factory: UIFactory) :
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    
    print(button.render())
    print(checkbox.toggle())

client_code(LightUIFactory())
client_code(DarkUIFactory())