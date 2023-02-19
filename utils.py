def parseIfNumber(value: str):
    if (value.replace('.', '').isdecimal()):
        return float(value)

    return value