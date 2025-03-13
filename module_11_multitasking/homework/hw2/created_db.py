import sqlite3

import logging.config

from utilits.logging.log_conf import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


class DataBase:

    def __init__(self, base_name: str, table: str):
        self.base_name = base_name
        self.name_table = table

    def connected_to_db(self):
        logger.debug(f'Подключаемся к базе данных: {self.base_name}')
        try:
            with sqlite3.connect(self.base_name) as client:
                logger.debug("Успешное подключение!")
                return client
        except Exception as e:
            logger.warning(f"не удалось подключится к {self.base_name}")
            logger.exception(e)

    def created_base(self):
        connect = self.connected_to_db()
        cur = connect.cursor()
        try:
            logger.debug(f'Создаем таблицу {self.name_table}')
            cur.execute(f'''
            CREATE TABLE {self.name_table} (
                id integer PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birth_year TEXT NOT NULL
                )
                ''')
            connect.commit()
            logger.info(f'База данных {self.name_table} - успешно создана')
        except Exception as err:
            logger.warning(f"Таблица {self.name_table} уже существует")
            logger.exception(err)

    def insert_data(self, data):
        connect = self.connected_to_db()
        cur = connect.cursor()
        try:
            logger.info(f"Записываем данные в {self.base_name}")
            cur.execute(
                f"INSERT INTO {self.name_table} (name, gender, birth_year) "
                f"VALUES (?, ?, ?)", data
            )
            connect.commit()
            logger.info(f"данные в {self.name_table} сохранены")
        except Exception as err:
            logger.warning(f"Не удачная попытка записать данные в {self.base_name}")
            logger.exception(err)

    def select_data(self):
        connect = self.connected_to_db()
        cur = connect.cursor()
        try:
            logger.info(f"Читаем данные с таблицы {self.name_table}")
            cur.execute(f'''SELECT * FROM {self.name_table}''')
            logger.info(f'Данные с таблицы {self.name_table} прочитаны')
            return cur.fetchall()
        except Exception as err:
            logger.warning(f"Не удалось прочитать данные с таблицы {self.name_table}")
            logger.exception(err)
