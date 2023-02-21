from pathlib import Path
from database import CSV
from algorithms.naive_bayes import NaiveBayes

ROOT_DIR = Path(__file__).parent

db = CSV(ROOT_DIR / 'credit.csv')

naiveBayes = NaiveBayes(db, 'risco')
prediction = naiveBayes.predict([
    ['boa', 'alta', 'nenhuma', 'acima_35'],
    ['ruim', 'alta', 'adequada', '0_15']
])

print(prediction)
