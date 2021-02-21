import logging


def setupLogger(name):

    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s: %(message)s',
            datefmt=date_format,
            filename='story.log'
        )

    logFormatter = logging.Formatter(
        fmt='%(asctime)s: %(message)s',
        datefmt=date_format
    )

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logFormatter)
    logging.getLogger('').addHandler(consoleHandler)

    return logging.getLogger(name)

