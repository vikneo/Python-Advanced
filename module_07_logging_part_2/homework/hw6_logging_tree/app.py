import os
import sys
from logging_tree import printout
import logging_tree
import logging.config
from utils import string_to_operator

logger = logging.getLogger('app')
logger.setLevel("DEBUG")
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

app_2 = logging.getLogger("app.app2")
app_2.setLevel("INFO")

handler = logging.StreamHandler(sys.stdout)
app_2.addHandler(handler)


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
    calc('6+3')
    
    file_name = os.path.join(os.path.dirname(__file__), "logging_tree.txt")
    printout()
    
    with open(file_name, "w")as file:
        file.write(logging_tree.format.build_description())


