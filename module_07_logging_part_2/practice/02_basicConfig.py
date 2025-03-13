import logging

root = logging.getLogger()

sub_1 = logging.getLogger("sub_1")
sub_1.setLevel("DEBUG")

sub_2 = logging.getLogger("sub_2")
sub_2.setLevel("DEBUG")
sub_2.propagate = False

sub_sub_1 = logging.getLogger("sub_2.sub_sub_1")
sub_sub_1.setLevel("DEBUG")

custom_handler = logging.StreamHandler()
root.addHandler(custom_handler)

custom_formatter = logging.Formatter('{levelname} || {name} || {message} || {module}.{funcName}:{lineno}', style = "{")
custom_handler.setFormatter(custom_formatter)


def main():
    print(root.handlers)
    print(sub_1.handlers)
    print(sub_2.handlers)
    print(sub_sub_1.handlers)
    sub_1.debug("message for sub_1")
    sub_2.debug("message for sub_2")
    sub_sub_1.debug("message for sub_sub_1")


if __name__ == '__main__':
    main()
