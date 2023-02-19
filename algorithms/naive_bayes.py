from database import Database
from functools import reduce

class NaiveBayes:
    def __init__(self, database: Database, target: str):
        self.database = database
        self.target = target
        
        self.checkErrors()
        
        self.probabilities = self.calculateProbabilities()
    
    def checkErrors(self):
        if self.target not in self.database.categories:
            raise Exception('Target not found in database')    
    
    def findAndCount(self, where: dict[int, int]):
        count = 0
        for line in self.database.parsedData:
            shouldCount = True
            for index in where:
                if line[index] != where[index]:
                    shouldCount = False
                    break
            
            if (shouldCount): 
                count += 1
            
        return count
    
    def calculateProbabilities(self):
        targetIndex = self.database.headers.index(self.target)
        
        targetCount = []
        
        for index in range(len(self.database.categories[self.target])):
            count = len([
                line[targetIndex] 
                for line in self.database.parsedData 
                if line[targetIndex] == index
            ])
        
            targetCount.append(count)
        
        for categorie in self.database.categories:
            if categorie == self.target:
                continue
        
            
            