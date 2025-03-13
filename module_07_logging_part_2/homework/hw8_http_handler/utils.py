
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging.config

from config_logger import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger('utils')

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    logger.info(f"Преобразование символа {value} в арифметическую функцию")
    logger.info(f"ASCII-filter did not miss the Cyrillic message in file '{__name__}'")
    if not isinstance(value, str):
        logger.error(f"wrong operator type {value}")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
