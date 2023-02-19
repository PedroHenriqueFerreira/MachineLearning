def parseIfNumber(value: str):
    '''
    Parse a string to a number if it is a number
    '''
    
    if (value.replace('.', '').isdecimal()):
        return float(value)

    return value

def parseToNumber(value: str | float):
    '''
    Parse a string to a number if it is a number or return 0
    '''
    
    if isinstance(value, float):
        return value

    return 0