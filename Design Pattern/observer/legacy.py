import time

class WeatherStation:
    def __init__(self):
        self._temp = 25
        self._has_changed = False

    def set_temperature(self, new_temp):
        if new_temp != self._temp:
            print(f"\n[WeatherStation] System Update: New temp is {new_temp}°C")
            self._temp = new_temp
            self._has_changed = True

    def get_temperature(self):
        self._has_changed = False # Reset flag after someone reads it
        return self._temp

    def check_for_update(self):
        return self._has_changed

class PhoneDisplay:
    def __init__(self, name):
        self.name = name

    def poll(self, station):
        if station.check_for_update():
            print(f"[{self.name}] detected change! Updating UI to {station.get_temperature()}°C")
        else:
            # This prints thousands of times if we don't sleep
            # print(f"[{self.name}] checking...") 
            pass

# --- The Messy Execution ---
station = WeatherStation()
phone = PhoneDisplay("iPhone 15")
tablet = PhoneDisplay("iPad Pro")

print("Starting Polling Loop... (Press Ctrl+C to stop)")

# This represents a "Game Loop" or a "Server Loop"
count = 0
try:
    while count < 5:
        # Every single device has to manually ask the station for data
        phone.poll(station)
        tablet.poll(station)
        
        # Simulate time passing and data changing
        if count == 2:
            station.set_temperature(30)
            
        time.sleep(1) # We wait 1 second, meaning updates are LAGGED
        count += 1
except KeyboardInterrupt:
    pass