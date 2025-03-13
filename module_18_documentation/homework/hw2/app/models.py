import os
import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys=ON;"

DATA_BOOKS = [
    {'title': 'A Byte of Python', 'author': 1},
    {'title': 'Moby-Dick; or, The Whale', 'author': 2},
    {'title': 'War and Peace', 'author': 3},
]

DATA_AUTHORS = [
    {'first_name': 'C', 'last_name': 'Swaroop', 'middle_name': 'H'},
    {'first_name': 'Herman', 'last_name': 'Melville', 'middle_name': ''},
    {'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': 'Nikolaevich'},
]

BASE_DIR = os.path.dirname(__file__)
DATABASE_NAME = 'table_books.db'
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[int] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author: Optional[Author]
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists_author = cursor.fetchone()
        if not exists_author:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name varchar(80) NOT NULL,
                    last_name varchar(80) NOT NULL,
                    middle_name varchar(80)
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (item['first_name'], item['last_name'], item['middle_name'])
                    for item in initial_records[1]
                ]
            )
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists_book = cursor.fetchone()
        if not exists_book:
            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title varchar(150) NOT NULL,
                    author INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records[0]
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id = row[0], title = row[1], author = row[2])


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id = row[0], first_name = row[1], last_name = row[2], middle_name = row[3])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_all_authors() -> list[Author]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHORS_TABLE_NAME}`')
        all_author = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_author]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, book.author.id)
        )
        book.id = cursor.lastrowid
        return book


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}`
            (first_name, last_name, middle_name) VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def update_author_by_id(author: Author) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {AUTHORS_TABLE_NAME}
            SET first_name = ?, last_name = ?, middle_name = ?
            WHERE id = ?
            """,
            (author.first_name, author.last_name, author.middle_name, author.id)
        )


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = 1")
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE id = ?
            """,
            (author_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_last_name(last_name: str) -> Optional[Author]:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE last_name = ?
            """,
            (last_name,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)