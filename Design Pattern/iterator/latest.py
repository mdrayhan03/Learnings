class RadioIterator :
    def __init__(self, radios):
        self._radios = radios
        self._index = 0

    def __next__(self):
        try :
            radio = self._radios[self._index]
            self._index += 1
            return radio
        except IndexError :
            raise StopIteration
        
class RadioStation :
    def __init__(self):
        self.stations = ["101.1 FM", "102.5 FM", "105.0 FM"]

    def __iter__(self):
        return RadioIterator(self.stations)
    
radio_station = RadioStation()

for radio in radio_station :
    print(radio)