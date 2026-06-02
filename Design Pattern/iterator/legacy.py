class RadioStation:
    def __init__(self):
        self.stations = ["101.1 FM", "102.5 FM", "105.0 FM"]

# Client Code
radio = RadioStation()
# The client HAS to know it's a list and use an index
for i in range(len(radio.stations)):
    print(radio.stations[i])