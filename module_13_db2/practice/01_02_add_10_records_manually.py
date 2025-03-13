import os
import sqlite3
import logging.config
from random import randint

from config.logger import dict_config
from config.base import created_table

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)

ADD_RECORDS = """ INSERT INTO 'table_warehouse' (name, description, amount) VALUES (?, ?, ?)"""


def add_10_records_to_table_warehouse(c: sqlite3.connect) -> None:
    cursor = c.cursor()
    try:
        for idx in range(10):
            cursor.execute(ADD_RECORDS,
                           (f'product_{idx + 1}', f'Simple description for product {idx + 1}', randint(0, 1000)))
            logger.info(f"Заносим в таблицу продукт с №-{idx + 1}")

        c.commit()
        logger.info(f"Внесенные данные сохранены")
    except Exception as err:
        c.commit()  # Стоит ли сохранять валидные данные до исключения?
        logger.error(f"Не удалось сохранить продукт с №-{idx + 1}\nОписание: {err}")


if __name__ == "__main__":
    with sqlite3.connect(path_to_db) as conn:
        add_10_records_to_table_warehouse(conn)
