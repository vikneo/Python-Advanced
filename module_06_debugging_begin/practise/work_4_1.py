"""
Перепишите банковский endpoint, заменив запись сообщений в файл на логирование.
Проверьте работу endpoint-а. Код этого задания мы будем использовать в следующем уроке,
поэтому обязательно выполните его перед изучением следующей темы
"""

import csv
from typing import Optional
import logging
import os
import re

from flask import Flask
from werkzeug.exceptions import InternalServerError

from created_dir import creted_dir_for_logs

app = Flask(__name__)

current_path = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    filename=os.path.join(creted_dir_for_logs(current_path, __file__), 'bank_api.log'),
    format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
)


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    file_name = f"{branch}.cs"
    branch_card_file_name = os.path.join(current_path, os.path.join("bank_data", file_name))
    logging.info(f'Search file {branch_card_file_name}')

    with open(branch_card_file_name, "r", encoding="utf-8") as fi:
        logging.info(f"Open file {fi} for read")
        csv_reader = csv.DictReader(fi, delimiter=",")
        logging.info(f"Reader file {csv_reader}")

        for record in csv_reader:
            if int(record["id"]) == person_id:
                logging.info(f"A value with id {person_id} was found")
                logging.info(f"We are returning {record['name']}")
                return record["name"]
        else:
            logging.warning(f"in file {file_name} person not found")
            return "Person not found", 404


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        logging.error(
                f"Tried to access {original.filename}. Exception info: {original.strerror}\n"
            )
    elif isinstance(original, OSError):
        logging.error(
            f"Unable to access a card. Exception info: {original.strerror}\n"
        )

    return "Internal server error", 500


if __name__ == "__main__":
    app.run()
