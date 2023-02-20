def parseIfNumber(value: str):
    if (value.replace('.', '').isdecimal()):
        return float(value)

    return value

def parseToNumber(value: str | float):
    if isinstance(value, float):
        return value

    return 0