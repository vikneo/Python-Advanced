import logging
import sys
from typing import Union, Callable
from operator import sub, mul, truediv, add

from errors import OperationError

util = logging.getLogger("util")
util.addHandler(logging.StreamHandler(sys.stdout))

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
        util.error(f"wrong operator type {value}")
        raise OperationError("wrong operator type")

    if value not in OPERATORS:
        util.error(f"Unsupported operator value {value}")
        raise OperationError("Unsupported operator value")

    return OPERATORS[value]
