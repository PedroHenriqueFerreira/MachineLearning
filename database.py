from abc import ABC, abstractmethod
from pathlib import Path
from parse import parseIfNumber, parseToNumber

class Database(ABC):
    def __init__(self, path: str | Path) -> None:
        self.path = path

        self.headers: list[str] = []
        self.categories: dict[str, list[str]] = {}

        self.data: list[list[str | float]] = []
        self.parsedData: list[list[int | float]] = []

        self.templateMethod()

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        className = self.__class__.__name__
        selfDict = self.__dict__
        attr = [
            f'\033[1m{attr}\033[0;0m={selfDict[attr]!r}' for attr in selfDict]
        formatedAttr = ', \n'.join(attr)

        return f'{className}(\n{formatedAttr}\n)'

    def templateMethod(self) -> None:
        self.read()
        self.checkErrors()

        self.setCategories()
        self.setParsedData()

    def checkErrors(self) -> None:
        if len(self.headers) == 0:
            raise Exception('Headers is empty')

        for row in self.data:
            if len(row) != len(self.headers):
                raise Exception('Data is invalid, check your data')

    def setCategories(self) -> None:
        for row in self.data:
            for i, item in enumerate(row):
                if isinstance(item, float):
                    continue

                if self.headers[i] not in self.categories:
                    self.categories[self.headers[i]] = [item]

                if item not in self.categories[self.headers[i]]:
                    self.categories[self.headers[i]].append(item)

    def setParsedData(self) -> None:
        ''' Not required, but it's a good practice to have a parsed data '''
        
        self.parsedData = [
            [parseToNumber(item) for item in row] for row in self.data
        ]

        for rowIndex, row in enumerate(self.data):
            for index, item in enumerate(row):
                if isinstance(item, float):
                    continue
                    
                numberValue = self.categories[self.headers[index]].index(item)

                self.parsedData[rowIndex][index] = numberValue

    @abstractmethod
    def read(self): ...


class CSV(Database):
    def read(self):
        with open(self.path, 'r') as file:
            data = file.readlines()

        for index, row in enumerate(data):
            values = row.strip().split(',')

            if index == 0:
                self.headers = values
                continue

            self.data.append([parseIfNumber(value) for value in values])
