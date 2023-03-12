from pathlib import Path
from database import CSV
from algorithms.naive_bayes import NaiveBayes

ROOT_DIR = Path(__file__).parent

# db = CSV(ROOT_DIR / 'credit.csv')

# naiveBayes = NaiveBayes(db, 'risco')
# prediction = naiveBayes.predict([
#     ['boa', 'alta', 'nenhuma', 'acima_35'],
#     ['ruim', 'alta', 'adequada', '0_15']
# ])

db = CSV(ROOT_DIR / 'teste.csv')

naiveBayes = NaiveBayes(db, 'sera_contratado')
prediction = naiveBayes.predict([
    ['não', '18_25', 'sim', 'não']
])


print(prediction)
