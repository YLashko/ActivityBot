import re 

number_filter = re.compile('^[-+]?([1-9]\d*|0)$')

def is_number(value):
    return number_filter.match(value)
