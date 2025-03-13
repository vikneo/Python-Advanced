import sqlite3
import os
import logging.config
from typing import Optional, List

from config.log_config import dict_config
from models import Book

from . import sql_commands as cmd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'table_books.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class DataBase:
    """
    The "DataBase" class is responsible for connecting
    to the database and contains "GRID" methods for operation
    """

    def __init__(self, base_name: str) -> None:
        logger.info(f'Initializing `table_books`')
        self.base_name = base_name
        self.connect = None
        self.cursor = self.__get_cursor()

    def init_db(self, filing_db: bool = False) -> None:
        self.cursor.execute(cmd.sql_exists)
        exists: Optional[tuple[str,]] = self.cursor.fetchone()
        if not exists:
            self.cursor.execute(cmd.sql_create_table)
            logger.info("Table `table_books` created successfully")

            if filing_db:
                self.cursor.executemany(
                    cmd.sql_create,
                    [
                        (item['title'], item['author'])
                        for item in DATA
                    ]
                )
                logger.info(f"The `table_books` table has been successfully filled with books")
            self.save()

    def __get_cursor(self) -> sqlite3.Cursor:
        with sqlite3.connect(self.base_name, check_same_thread = False) as conn:
            logger.info(f'Connected to database `table_books`')
            self.connect = conn
            cursor: sqlite3.Cursor = self.connect.cursor()
            logger.info(f'Getting the cursor object')
            return cursor

    def all(self) -> list[Book]:
        data = self.cursor.execute(cmd.sql_select_all)
        logger.info(f'All data from the `table_books` database has been received')
        return [Book(*row) for row in data.fetchall()]

    def create(self, table_name: str) -> None:
        """ Creates object in the database """
        self.cursor.execute(cmd.sql_create, table_name)
        logger.info(f'Data from `{table_name}` has been successfully added')
        self.save()

    def update(self, **kwargs: dict) -> None:
        """ Updates object in the database """

        if 'id' in kwargs:
            self.cursor.execute(cmd.sql_update_view, (kwargs['id'],))
            logger.info(f'Data for `book-{kwargs["id"]}` has been successfully updated')
        else:
            self.cursor.execute(cmd.sql_update_views)
            logger.info(f'Views for books has been successfully updated')
        self.save()

    def delete(self, data: str) -> None:
        """ Deletes object in the database """
        ...

    def filter(self, data: str) -> List:
        """ Filters object in the database """
        books = self.cursor.execute(cmd.sql_select_filter, ("{}%".format(data),))
        logger.info(f'The list of objects from the database was obtained using the method')
        return [Book(*row) for row in books.fetchall()]

    def get(self, **kwargs: dict) -> Book:
        """ Returns object from the database """
        book = self.cursor.execute(cmd.sql_select_get, (kwargs['id'],))
        logger.info(f'An object was obtained from the database using the method `get`')
        return Book(*book.fetchone())

    def save(self) -> None:
        logger.info(f'Saving data to database `table_books`')
        self.connect.commit()


object_db = DataBase(path_to_db)
