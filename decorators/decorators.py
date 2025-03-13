"""
Здесь будут жить декораторы. Например: время работы функции...

Decorators will live here
"""
import logging
import time

logging.basicConfig(level=logging.INFO)


def time_tracker(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round(time.time() - start, 4)
        logging.warning(f"'{func.__name__}' - took {end:.2f} seconds")
        return result
    return wrapper

