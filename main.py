from pathlib import Path
from database import CSV
from algorithms.naive_bayes import NaiveBayes

ROOT_DIR = Path(__file__).parent

db = CSV(ROOT_DIR / 'credit.csv')

NaiveBayes(db, 'risco')