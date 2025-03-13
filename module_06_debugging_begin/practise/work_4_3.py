"""
Представим, что мы работаем в IT отделе крупной компании.
У HR отдела появилась гениальная идея - поздравлять сотрудников
в день рождения однодневным отгулом.

Для этого HR отделу надо предоставить данные на всех
сотрудников вместе с их датами рождения.
Сотрудники у нас работают либо в IT-, либо в PROD-отделе.
Идентификационным номером сотрудника является число,
анкеты сотрудников в формате json вы можете найти в папке fixtures.
В написанное приложение добавьте логи так,
чтобы они помогли найти ошибки со следующими сотрудниками
    отдел IT, сотрудники 1, 2, 3, 4, 5
    отдел PROD, сотрудники 1, 2, 3, 4, 5
"""

import json
from json import JSONDecodeError
import logging
import os
from datetime import datetime

from flask import Flask

from created_dir import creted_dir_for_logs

app = Flask(__name__)

logger = logging.getLogger("account_book")

current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

departments = {"IT": "it_dept", "PROD": "production_dept"}


@app.route("/account/<department>/<int:account_number>/")
def account(department: str, account_number: int):
    dept_directory_name = departments.get(department)

    if dept_directory_name is None:
        logger.warning(f"Department {dept_directory_name} not found")
        return "Department not found", 404

    full_department_path = os.path.join(fixtures_dir, dept_directory_name)

    account_data_file = os.path.join(full_department_path, f"{account_number}.json")

    with open(account_data_file, "r", encoding="utf-8") as fi:
        account_data_txt = fi.read()

    account_data_json = json.loads(account_data_txt)

    name, birth_date = account_data_json["name"], account_data_json["birth_date"]
    day, month, _ = birth_date.split(".")

    if not name:
        logger.warning(f"Сотрудник не определен! Проверте данные о сотрудниках")
    
    if int(_) > datetime.today().year:
        logger.error(f"Не коректная дата рождения {_} г.! Возможно опечатка!")

    if not (1 < int(day, 10) < 31) or not (1 < int(month, 10) < 12):
        raise ValueError
    
    return f"{name} was born on {day}.{month}"


@app.errorhandler(JSONDecodeError)
def handle_exception(err: JSONDecodeError):
    """
    
    """
    logger.error(f"Не верные данные в файле JSON: - {err}")

    return "Не верные данные в файле JSON", 400


@app.errorhandler(KeyError)
def handle_exception(err: KeyError):
    """
    
    """
    logger.error(f"Получен не верный ключ из файла json: - {err}")

    return "Не верный ключ в файле", 400


@app.errorhandler(FileNotFoundError)
def handle_exception(err: FileNotFoundError):
    """
    
    """
    logger.error(f"Отсутсвует указанный файл: - {err}")

    return "Отсутствует файл", 400


@app.errorhandler(ValueError)
def handle_exception(err: ValueError):
    """
    
    """
    logger.error(f"Не верно указана дата рождения: - {err}")

    return "Не верные данные в дате", 400




if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        encoding='utf-8',
        filename=os.path.join(creted_dir_for_logs(current_dir, __file__), "it_compani_log.log"),
        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
        )
    logger.info("Started account server")
    app.run(debug=True)
