from datetime import datetime
from functools import reduce


def get_timestamp():
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    return ts


def dict_len(dictionary):
    values_lengths = [len(v) for v in dictionary.values()]
    return reduce(lambda a, b: a + b, values_lengths)
