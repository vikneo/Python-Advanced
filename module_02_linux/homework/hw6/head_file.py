"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

docs/simple.txt:
hello world!

/preview/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/preview/100/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""
import os
from flask import Flask

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str) -> str:
    """
    Функция выводит из файла количество символов по значению size
    :param size: кол-во символов
    :param relative_path: название файла
    :return: str
    """
    path_dir = os.path.dirname(__file__)
    response = os.path.join(path_dir, relative_path)
    try:
        with open(response, 'r', encoding='utf-8') as file:
            return f"<b>{path_dir}</b>" \
                   f"<p>{path_dir} {size}</p>" \
                   f"<p>{file.read(size)}</p>"
    except Exception as err:
        return f'Данный файл в директории "{__file__}" <b>отсутствует</b>.' \
               f"<p>Описание ошибки: {err}</p>"


if __name__ == "__main__":
    app.run(debug=True)
