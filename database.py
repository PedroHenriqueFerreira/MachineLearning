from abc import ABC, abstractmethod
from pathlib import Path

class Database(ABC):
    def __init__(self, path: str | Path) -> None:
        self.path: str | Path = path

        self.headers: list[str] = []
        self.categories: dict[str, list[str]] = {}

        self.data: list[list[str]] = []
        self.parsedData: list[list[int]] = []

        self.templateMethod()

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
        self.parseData()

    def checkErrors(self) -> None:
        if len(self.headers) == 0:
            raise Exception('Headers is empty')

        for line in self.data:
            if len(line) != len(self.headers):
                raise Exception('Data is invalid')

    def setCategories(self) -> None:
        for line in self.data:
            for i, item in enumerate(line):
                if self.headers[i] not in self.categories:
                    self.categories[self.headers[i]] = [item]

                if item not in self.categories[self.headers[i]]:
                    self.categories[self.headers[i]].append(item)

    def parseData(self) -> None:
        parsedData: list[list[int]] = [[0 for _ in line] for line in self.data]

        for lineIndex, line in enumerate(self.data):
            for i, item in enumerate(line):
                numberValue = self.categories[self.headers[i]].index(item)

                parsedData[lineIndex][i] = numberValue

        self.parsedData = parsedData

    @abstractmethod
    def read(self): ...


class CSV(Database):
    def read(self):
        with open(self.path, 'r') as file:
            data = file.readlines()

        for i, line in enumerate(data):
            values = line.strip().split(',')

            if i == 0:
                self.headers = values
                continue

            self.data.append(values)
