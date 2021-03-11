from datetime import datetime


def get_timestamp():
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    return ts
