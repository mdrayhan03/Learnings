class LightButton:
    def render(self): return "Rendering White Button"

class DarkButton:
    def render(self): return "Rendering Charcoal Button"

class LightCheckbox:
    def toggle(self): return "Checking Light Box"

class DarkCheckbox:
    def toggle(self): return "Checking Dark Box"

# --- The Messy Client ---
def create_ui(theme):
    if theme == "light":
        btn = LightButton()
        chk = LightCheckbox()
    else:
        btn = DarkButton()
        chk = DarkCheckbox()
    
    print(btn.render())
    print(chk.toggle())