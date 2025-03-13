"""
Запустите локально пример с bank_api.
Попробуйте с помощью разных комбинаций параметров добиться того,
чтобы была выполнена каждая строчка кода - мы должны попасть во все функции,
в каждый if и for блок.

Чтобы достоверно проверить выполнение каждой строчки кода,
можно добавить после каждого выражения запись в файл вида "строка такая-то была посещена"...
"""
import csv
import os
from typing import Optional
import traceback

from flask import Flask
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

current_dir = os.path.abspath(os.path.dirname(__file__))


def check_sting_code(message: str) -> None:
    """
    Checking the visit to each page of the code and writing to a file
    """
    file_name = "work_2_1_check_string_code.txt"
    with open(f"{current_dir}/errors/{file_name}", "a", encoding="utf-8") as file:
        file.writelines(message)


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    branch_card_file_name = os.path.join(current_dir, f"bank_data/{branch}.csv")
    check_sting_code(f"строка {traceback.extract_stack()[-1].lineno} (найден файл: {branch}.csv) - была посещена\n")

    with open(branch_card_file_name, "r") as fi:
        check_sting_code(
            f"строка {traceback.extract_stack()[-1].lineno} (открыт файл на чтение: {branch}.csv) - была посещена\n")
        csv_reader = csv.DictReader(fi, delimiter=",")
        check_sting_code(
            f"строка {traceback.extract_stack()[-1].lineno} (прочитан файл: {branch}.csv) - была посещена\n")

        for i, record in enumerate(csv_reader):
            check_sting_code(f"строка {traceback.extract_stack()[-1].lineno} (вошли в цикл 'for') - была посещена\n")
            if int(record["id"]) == person_id:
                check_sting_code(
                    f"строка {traceback.extract_stack()[-1].lineno} (найден id: {person_id}) - была посещена\n")
                check_sting_code(
                    f"строка {traceback.extract_stack()[-1].lineno} "
                    f"(найдено имя: {record['name']}) - была посещена\n{'=' * 20}\n")
                return record["name"]
            check_sting_code(
                f"строка {traceback.extract_stack()[-1].lineno} (закончена {i}-я итерация) - была посещена\n")
        else:
            check_sting_code(f"строка {traceback.extract_stack()[-1].lineno} (Имя не найдено) - была посещена\n")
            return "Person not found", 404


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        with open("invalid_error.log", "a") as fo:
            fo.write(
                f"Tried to access {original.filename}. Exception info: {original.strerror}\n"
            )
    elif isinstance(original, OSError):
        with open("invalid_error.log", "a") as fo:
            fo.write(f"Unable to access a card. Exception info: {original.strerror}\n")

    return "Internal server error", 500


if __name__ == "__main__":
    app.run()
