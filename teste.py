import numpy as np

from sklearn.naive_bayes import GaussianNB

def likelyhood(y: list[float], Z: list[list[float | int]]):
    def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2) / (2 * np.power(sig, 2)))
    
    prob = 1
    for index, item in enumerate(Z):
        m = np.mean(item)
        s = np.std(item)      
        prob = prob * gaussian(y[index], m, s)
    return prob

print(likelyhood([9, 10, 11], [[4, 5, 6], [7, 8, 9]]))