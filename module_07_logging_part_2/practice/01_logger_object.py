import logging

root = logging.getLogger()
main = logging.getLogger('main')
main.setLevel("INFO")
utils = logging.getLogger('utils')
utils.setLevel("DEBUG")


def main_logger():
    print(root)
    print(main)
    print(utils)


if __name__ == '__main__':
    main_logger()
