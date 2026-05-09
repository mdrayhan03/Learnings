from abc import ABC, abstractmethod

class Database(ABC) :
    @abstractmethod
    def get_data(self, key, password) : pass

class RealDatabase(Database) :
    def __init__(self):
        print("--- Connecting to heavy Database... ---")
        self.data = {
                        "12345": "John Doe", 
                        "12346": "John Poe", 
                        "12347": "John Loe", 
                    }

    def get_data(self, key):
        return self.data.get(key)

class ProxyDatabase(Database) :
    def __init__(self):
        print("--- Connecting to proxy Database... ---")
        self._real_db = None
        self.password = '1234'

    def get_data(self, key, password) : 
        if self.password == password :
            if self._real_db is None :
                self._real_db = RealDatabase()
            data = self._real_db.get_data(key)
            print(data)
        else :
            print("Wrong Password.")

db = ProxyDatabase()
db.get_data("12345", "1234")