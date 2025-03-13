import inspect
from termcolor import cprint


def treeclass(cls, ind: int = 0):
    if ind == 3:
        print(f'{"|"}{"_" * ind}', end="")
    if ind == 6:
        print(f'{"|"}{" " * ind}{"|"}{"_" * ind}', end="")
    if ind == 9:
        print(f'{"|"}{" " * (ind - 3)}{"|"}{" " * ind}{"|"}{"_" * ind}', end="")

    cprint(f"{cls.__name__}  ", 'yellow', attrs=['bold'])

    for i in cls.__subclasses__():
        treeclass(i, ind + 3)


# noinspection PyTypeChecker
inspect.getclasstree(inspect.getmro(BaseException))

if __name__ == '__main__':
    treeclass(BaseException)
