from typing import Union, Callable
from operator import sub, mul, truediv, add

from errors import OperationError
from setup_logger import get_logger


util_log = get_logger("util")


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
    if not isinstance(value, str):
        util_log.error(f"wrong operator type {value}")
        raise OperationError("wrong operator type")

    if value not in OPERATORS:
        util_log.error(f"Unsupported operator value {value}")
        raise OperationError("Unsupported operator value")

    return OPERATORS[value]
