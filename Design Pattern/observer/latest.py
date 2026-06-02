import time

class WeatherStation:
    def __init__(self):
        self._temp = 25
        self._observers = []
    
    def attach(self, observer) :
        self._observers.append(observer)
    
    def detach(self, observer) :
        pass

    def set_temperature(self, new_temp):
        if new_temp != self._temp:
            print(f"\n[WeatherStation] System Update: New temp is {new_temp}°C")
            self._temp = new_temp
            self.notify()

    def notify(self) :
        if len(self._observers) > 0 :
            for observer in self._observers :
                observer.update(self._temp)

class PhoneDisplay:
    def __init__(self, name):
        self.name = name

    def update(self, temperature):
        print(f"[{self.name}] detected change! Updating UI to {temperature}°C")

# --- The Messy Execution ---
station = WeatherStation()
phone = PhoneDisplay("iPhone 15")
tablet = PhoneDisplay("iPad Pro")

station.attach(phone)
station.attach(tablet)

print("Starting Polling Loop... (Press Ctrl+C to stop)")

# This represents a "Game Loop" or a "Server Loop"
count = 0
try:
    while count < 5:
        if count == 2:
            station.set_temperature(30)
            
        time.sleep(1) # We wait 1 second, meaning updates are LAGGED
        count += 1
except KeyboardInterrupt:
    pass