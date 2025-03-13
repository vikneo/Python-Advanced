import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config
from command_uefa import generate_command_list, create_commands_uefa, insert_command_uefa

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


class UEFADataBase:
    """
    Не универсальный класс для создания таблиц и заполнения данными команд для задачи hw5
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connect = None
        self.table = 'uefa_commands'
        self.cursor = self.connect_to_db()

    def connect_to_db(self) -> sqlite3.Cursor:
        with sqlite3.connect(self.db_name) as connect:
            cursor = connect.cursor()
            self.connect = connect
            logger.info('Connected to database')
            return cursor

    def create(self) -> None:
        try:
            self.cursor.executescript(create_commands_uefa)
            logger.info(f'create tables `uefa_commands` and `uefa_draw`')
        except sqlite3.OperationalError as err:
            pass
        except Exception as _err:
            logger.warning(_err)
            logger.exception(_err)

        self.insert(insert_command_uefa, generate_command_list)

    def insert(self, sql_request: str, data: list[tuple[int, str, str, str]], table_name: str = None) -> None:
        try:
            self.cursor.executemany(sql_request, data)
            logger.info(f'insert data into `{table_name if table_name is not None else self.table}`')
            self.connect.commit()
            logger.info(f'Save data into `{table_name}`')
        except Exception:
            pass


database = UEFADataBase(path_to_db)
