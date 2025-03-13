import sqlite3
import os
import logging.config

from config.logger import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

def created_table(connect: sqlite3.Cursor, name_table: str, fields: str) -> None:
    cur = connect.cursor()
    try:
        logger.debug(f'Создаем таблицу {name_table}')
        cur.execute(f''' CREATE TABLE {name_table} ({fields}) ''')
        connect.commit()
        logger.info(f'База данных {name_table} - успешно создана')
    except Exception as err:
        logger.warning(f"Таблица {name_table} уже существует")
