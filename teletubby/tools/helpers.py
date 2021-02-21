from datetime import datetime
import logging


def get_timestamp():
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    return ts


def printDebug(*args, name='bouncer'):
    myLogger = logging.getLogger(name)
    message = ' '.join([str(arg) for arg in args])
    myLogger.debug(message)

