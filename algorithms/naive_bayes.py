from database import Database
from functools import reduce


class NaiveBayes:
    def __init__(self, database: Database, target: str):
        self.database = database
        self.target = target
        
        self.probabilityTable: dict[str, dict[str, dict[str, int]]] = {}
        self.targetProbability: dict[str, int] = {}

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

    def checkErrors(self):
        if self.target not in self.database.categories:
            raise Exception('Target not found in database')

    def calculateProbabilities(self) -> None:
        targetIndex = self.database.headers.index(self.target)

        for index, targetString in enumerate(self.database.categories[self.target]):
            count = self.findAndCount({ targetIndex: index })
            self.targetProbability[targetString] = count

        for categorie in self.database.categories:
            if categorie == self.target:
                continue
            
            self.probabilityTable[categorie] = {}
            categorieIndex = self.database.headers.index(categorie)

            for categorieValue, categorieString in enumerate(self.database.categories[categorie]):
                self.probabilityTable[categorie][categorieString] = {}

                for targetValue, targetString in enumerate(self.database.categories[self.target]):
                    
                    categorieCount = self.findAndCount({
                        targetIndex: targetValue,
                        categorieIndex: categorieValue
                    })

                    self.probabilityTable[categorie][categorieString][targetString] = categorieCount

    def predict(self, data: list[list[str | float]]):
        print(self.database)
        print(self)