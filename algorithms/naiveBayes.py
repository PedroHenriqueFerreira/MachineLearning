from database import Database

class NaiveBayes:
    def __init__(self, database: Database):
        self.database = database
        self.probabilities = self.calculateProbabilities()
        
    def calculateProbabilities(self):
        print(self.database)