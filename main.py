from pathlib import Path
from database import CSV

ROOT_DIR = Path(__file__).parent

db = CSV(ROOT_DIR / 'credit.csv')
print(db)