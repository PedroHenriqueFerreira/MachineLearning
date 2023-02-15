from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self, path):
        self.path = path
        self.header = None
        self.data = []
        
        self.read()
    
    @abstractmethod
    def read(self): ...

class CSVDatabase(Database):
    def read(self):
        with open(self.path, 'r') as file:
            data = file.readlines()

        for i, line in enumerate(data):
            values = line.strip().split(',')
            
            if i == 0:
                self.header = values
                continue
        
            self.data.append(values)

csv = CSVDatabase('./database.csv')