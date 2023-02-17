from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self, path: str):
        self.path: str = path
        self.header: list[str] = []
        self.data: list[list[str]] = []
        self.categories: dict[str, list[str]] = {}
        self.parsedData: list[list[int]] = []
        
        self.read()
        self.setCategories()
        self.setParsedData()
    
    def __str__(self) -> str:
        className = self.__class__.__name__
        selfDict = self.__dict__
        attributes =  ', '.join([f'{attr}={selfDict[attr]!r}' for attr in selfDict])
        
        return f'{className}({attributes})'
    
    def setCategories(self):
        for line in self.data:
            for i, item in enumerate(line):
                if self.header[i] not in self.categories:
                    self.categories[self.header[i]] = [item]
                    
                if item not in self.categories[self.header[i]]:
                    self.categories[self.header[i]].append(item)
    
    def setParsedData(self):
        newData: list[list[int]] = [line[:] for line in self.data]
        
        for lineIndex, line in enumerate(self.data):
            for i, item in enumerate(line):
                if self.header[i] not in self.categories:
                    raise Exception(f'Header {self.header[i]} not found in categories')
                
                if (item not in self.categories[self.header[i]]):
                    raise Exception(f'Item {item} not found in categories')
                
                numberValue = self.categories[self.header[i]].index(item)
                
                newData[lineIndex][i] = numberValue
                
        print(self.categories)
        print(newData)
        print(self.data)
        
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
     
       
CSVDatabase('./credit.csv')