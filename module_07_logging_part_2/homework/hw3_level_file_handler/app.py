
from logger_helper import get_logger
from utils import string_to_operator

logger = get_logger("app")


def calc(args):
    logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.exception(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")
    logger.critical("Program shutdown")


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('a+3')
