from math import log2
from functools import reduce

def entropy(*values):
    def reducer(ac, value):
        if value == 0:
            return ac
        
        return ac - value * log2(value)
    
    return reduce(reducer, values, 0)
    

print(entropy(1/3, 2/3))