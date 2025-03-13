import datetime
import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

create_table_birds = """
CREATE TABLE `table_birds` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    date_time NUMERIC NOT NULL,
    count INTEGER NOT NULL
);
"""

checking_bird = """
SELECT EXISTS (SELECT name FROM 'table_birds' WHERE name=?);
"""

added_bird_to_base = """
INSERT INTO 'table_birds' (name, date_time, count) VALUES (?, ?, ?)
"""


def log_bird(
        cur: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
        count_bird: int,
) -> None:
    data = (bird_name, date_time, count_bird)
    if check_if_such_bird_already_seen(cur, bird_name):
        logger.info(f'Птицу {bird_name} мы уже наблюдали!')
        return

    cur.execute(added_bird_to_base, data)
    logger.info(f"Птица {bird_name} - добавлена в базу")


def check_if_such_bird_already_seen(
        cur: sqlite3.Cursor,
        bird_name: str
) -> bool:
    result = cur.execute(checking_bird, (bird_name,))
    return result.fetchone()[0]


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ").capitalize()
    count: int = int(input("Сколько птиц вы увидели?\n> "))
    right_now: str = datetime.datetime.now(datetime.UTC).isoformat()

    with sqlite3.connect(path_to_db) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        try:
            cursor.execute(create_table_birds)
            logger.info('Create data base named `table_birds`')
        except sqlite3.OperationalError:
            pass
        except Exception as err:
            logger.warning(err)

        log_bird(cursor, name, right_now, count)
