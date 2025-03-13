"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FILE = os.path.join(BASE_DIR, 'output.txt')


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Функция открывает файл, подсчитывает количество занимаемой
    памяти в запущенных процессах.
    :param ps_output_file_path: путь к файлу,
    :return: результат в байтах
    """
    __total = 0
    __file = os.path.basename(ps_output_file_path)
    __Kb = 1024

    try:
        with open(ps_output_file_path, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                item = line.split()[5]
                if item.isdigit():
                    __total += int(item)
    except Exception as err:
        return f'Файла "{__file}" не существует.\nОписание ошибки: {err}'

    return f'Размер файла {__file}:\n' \
           f'В Байтах: {__total} B;\n' \
           f'В Килобайтах: {__total / __Kb} Kb;\n' \
           f'В Мегабайтах: {__total / (__Kb ** 2)} Mb;\n' \
           f'В Гигабайтах: {__total / (__Kb ** 3)} Gb;'


if __name__ == '__main__':
    path: str = BASE_FILE
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
