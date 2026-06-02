class RadioStation :
    def __init__(self):
        self.stations = ["101.1 FM", "102.5 FM", "105.0 FM"]

    def __iter__(self):
        for station in self.stations :
            yield station
    
radio_station = RadioStation()

for radio in radio_station :
    print(radio)