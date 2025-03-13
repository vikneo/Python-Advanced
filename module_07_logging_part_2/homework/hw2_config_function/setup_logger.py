import sys
import logging


def get_logger(name: str, propagate = False, stream = True):
    log = logging.getLogger(name)
    logging.basicConfig(level=logging.DEBUG)
    log.propagate = propagate

    handler = logging.StreamHandler(sys.stdout if stream else sys.stderr)
    formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s')

    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
