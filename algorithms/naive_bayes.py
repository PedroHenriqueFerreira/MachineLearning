from database import Database
from functools import reduce


class NaiveBayes:
    def __init__(self, database: Database, target: str):
        self.database = database
        self.target = target
        
        self.probabilityTable: dict[str, dict[str, dict[str, int]]] = {}
        self.targetProbability: dict[str, int] = {}
        self.dataLength = len(self.database.data)

        self.templateMethod()

    def __str__(self) -> str:
        className = self.__class__.__name__
        selfDict = self.__dict__
        attr = [
            f'\033[1m{attr}\033[0;0m={selfDict[attr]!r}' for attr in selfDict]
        formatedAttr = ', \n'.join(attr)

        return f'{className}(\n{formatedAttr}\n)'

    def templateMethod(self) -> None:
        self.checkErrors()
        self.calculateProbabilities()

    def findAndCount(self, where: dict[str, str]):
        count = 0
        for row in self.database.data:
            shouldCount = True

            for key in where:
                keyIndex = self.database.headers.index(key)

                if row[keyIndex] != where[key]:
                    shouldCount = False
                    break

            if (shouldCount):
                count += 1

        return count

    def checkErrors(self):
        if self.target not in self.database.categories:
            raise Exception('Target not found in database')

    def correctCount(self, targetItem: str, count: int) -> int:
        if count != 0:
            return count
        
        self.dataLength += 1
        self.targetProbability[targetItem] += 1
        
        return count + 1
        
    def calculateProbabilities(self) -> None:
        for targetItem in self.database.categories[self.target]:
            count = self.findAndCount({self.target: targetItem})
            self.targetProbability[targetItem] = count

        for categorie in self.database.categories:
            if categorie == self.target:
                continue

            self.probabilityTable[categorie] = {}

            for categorieItem in self.database.categories[categorie]:
                self.probabilityTable[categorie][categorieItem] = {}

                for targetItem in self.database.categories[self.target]:

                    count = self.findAndCount({
                        self.target: targetItem,
                        categorie: categorieItem
                    })
                    
                    # newCount = self.correctCount(targetItem, count)

                    self.probabilityTable[categorie][categorieItem][targetItem] = count

    def predict(self, data: list[list[str | float]]):
        results: list[str] = []
        
        for row in data:
            probabilities: dict[str, float] = {}
            
            for index, categorie in enumerate(self.database.categories):
                divisor = None
                
                if categorie == self.target:
                    targetProbability = self.targetProbability
                    divisor = self.dataLength
                else:
                    targetProbability = self.probabilityTable[categorie][str(row[index])]
                
                for targetItem in targetProbability:
                    if not divisor:
                        divisor = self.targetProbability[targetItem]
                        
                    fraction = targetProbability[targetItem] / divisor
                    
                    if targetItem in probabilities:
                        probabilities[targetItem] *= fraction
                    else:
                        probabilities[targetItem] = fraction
                        
            maxValue = 0.0
            maxName = ''
            
            for probability in probabilities:
                if probabilities[probability] > maxValue:
                    maxValue = probabilities[probability]
                    maxName = probability
                    
            results.append(maxName)
            
        return results