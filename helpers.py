def extract_int(string):
    """remove all non-digit characters and convert the rest to integer"""
    return int(''.join([x for x in string if x in "0123456789"]))

