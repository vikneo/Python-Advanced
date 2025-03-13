import sqlite3
import os
import logging.config

from config.logger import dict_config

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)

ADD_RECORDS = """ INSERT INTO 'table_books' (isbn, book_name, author, publish_year) VALUES (?, ?, ?, ?)"""


def add_books_from_file(c: sqlite3.connect, file_name: str) -> None:
    with open(file_name) as file:
        cursor = c.cursor()
        try:
            for book in file.readlines()[1:]:
                data = book.rstrip('\n').split(',')
                cursor.execute(ADD_RECORDS, data)
                logger.info(f"Заносим в таблицу книгу с артикулом - {data[0]}")

            c.commit()
            logger.info(f"Внесенные данные сохранены")
        except Exception as err:
            c.commit()  # Стоит ли сохранять валидные данные до исключения?
            logger.error(f"Не удалось сохранить книгу с артикулом - {data[0]}\nОписание: {err}")


if __name__ == "__main__":
    book_list = os.path.join(BASE_DIR, "book_list.csv")
    with sqlite3.connect(path_to_db) as conn:
        add_books_from_file(conn, book_list)
