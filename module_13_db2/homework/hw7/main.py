import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


def register(username: str, password: str) -> None:
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "I like"
    password: str = ("SQL Injection'); "
                     "UPDATE table_users SET username = replace(username, 'Лебедева Т.Ч.', 'shadowman') "
                     "WHERE username='Лебедева Т.Ч.';--")
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
