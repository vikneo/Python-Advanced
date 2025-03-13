import sqlite3
import os
from typing import List
import logging.config

from config.logger import dict_config

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)

defeated_enemies = [
    "Иванов Э.",
    "Петров Г.",
    "Левченко Л.",
    "Михайлов М.",
    "Яковлев Я",
    "Кузнецов К.",
]

sql_del_person = """
DELETE FROM table_enemies WHERE name=?
"""


def remove_all_defeated_enemies(
        c: sqlite3.Cursor,
        defeated_enemies: List[str]
) -> None:
    for name in defeated_enemies:
        c.execute(sql_del_person, (name,))
        logger.info(f"Соперник {name} побежден, удаляем из таблицы")


if __name__ == "__main__":
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()
        remove_all_defeated_enemies(cursor, defeated_enemies)
        conn.commit()
        logger.info("Побежденные соперники удалены из таблицы. Сохраняем изменения!")
