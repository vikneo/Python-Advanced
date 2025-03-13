from setup_logger import get_logger
from utils import string_to_operator

from errors import OperationError, NumericError

app_log = get_logger("app")


def convert_numbers(num1, num2) -> list[float]:

    try:
        num_1 = float(num1)
    except ValueError as e:
        raise NumericError(f"Error while converting number 1: {e}")

    try:
        num_2 = float(num2)
    except ValueError as e:
        raise NumericError(f"Error while converting number 2: {e}")

    return [num_1, num_2]


def calc(args):
    app_log.debug(f"Arguments: {args}")

    try:
        num1 = args[0]
        operator = args[1]
        num2 = args[2]

        num_1, num_2 = convert_numbers(num1, num2)
        operator_func = string_to_operator(operator)
        result = operator_func(num_1, num_2)

        app_log.info(f"Result: {result}")
        app_log.info(f"{num_1} {operator} {num_2} = {result}")
    except NumericError as e:
        app_log.exception(e)
    except OperationError as e:
        app_log.exception(f"Error: {e}")
    except IndexError as e:
        app_log.exception(e)


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('9-6')
