import logging.config
import sqlite3
import os
import logging

from config.logger import dict_config

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)

number_of_hurricane_days = """
    SELECT COUNT(*) as count FROM 'table_kotlin' WHERE wind >= ?;
"""


def hurricane_day_counter(c: sqlite3.connect, wind: int) -> tuple:
    """
    Подсчет дней с ураганом на острове Котлин
    """
    cursor = c.cursor()
    cursor.execute(number_of_hurricane_days, (wind,))
    result = cursor.fetchone()
    logger.info(f"На острове Котлин ураганных дней составило - {result[0]} дней ")
    return result


if __name__ == "__main__":
    with sqlite3.connect(path_to_db) as conn:
        res = hurricane_day_counter(conn, 33)
        print(f"+{'':-^10}+")
        print(f"|{'count':^10}|")
        print(f"+{'':-^10}+")
        print(f"|{res[0]:^10}|")
        print(f"+{'':-^10}+")