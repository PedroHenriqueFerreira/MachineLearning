from pathlib import Path
from database import CSVDatabase

ROOT_DIR = Path(__file__).parent

db = CSVDatabase(ROOT_DIR / 'credit.csv')

# from print import print

print(db)