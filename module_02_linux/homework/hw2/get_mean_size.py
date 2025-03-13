"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: list) -> float:
    """
    Функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
    а возвращает средний размер файла в каталоге.
    :param ls_output: list список строк после выполнения команды ls -l
    :return: float средний размер файла в каталоге.
    """
    size = 0
    try:
        for _str in ls_output:
            size_file = int(_str.split()[4])
            size += size_file
        return size / len(ls_output)
    except Exception:
        raise FileNotFoundError


if __name__ == '__main__':
    data: list = sys.stdin.readlines()[1:]
    try:
        mean_size: float = get_mean_size(data)
        print(f"Средний размер файлов {mean_size} kb ")
    except FileNotFoundError:
        print("Данный каталог пустой или не существует")
    except Exception:
        print("Ошибка в данных")
