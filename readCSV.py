class CSV:
    def __init__(self, path):
        self.path = path
        self.data = self.file.readlines()
        
    def read(self):
        with open(self.path) as file:
            self.file = file
            return self.data

with open('./database.csv') as file:
    for line in file.readlines():
        myLine = line.strip()
        print(myLine)
    
