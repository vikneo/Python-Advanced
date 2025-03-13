import os
import sqlite3

import insert_sql_cmd  as cmd_sql

BASE_DIR = os.path.dirname(__file__)
base_name = "movie_lib.db"
path_to_db = os.path.join(BASE_DIR, base_name)


create_table_director = """
    DROP TABLE IF EXISTS 'director';
    CREATE TABLE 'director' (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
    )
"""

create_table_movie = """
    DROP TABLE IF EXISTS 'movie';
    CREATE TABLE 'movie' (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
    )
"""

create_table_actors = """
    DROP TABLE IF EXISTS 'actors';
    CREATE TABLE 'actors' (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_lst_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
    )
"""

create_table_movie_director = """
    DROP TABLE IF EXISTS 'movie_director';
    CREATE TABLE 'movie_director' (
    dir_id INTEGER,
    mov_id INTEGER,
    FOREIGN KEY (dir_id) REFERENCES director (dir_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE,
    PRIMARY KEY (dir_id, mov_id)
    )
"""

create_table_movie_cast = """
    DROP TABLE IF EXISTS 'movie_cast';
    CREATE TABLE 'movie_cast' (
    act_id INTEGER,
    mov_id INTEGER,
    role VARCHAR(50) NOT NULL,
    FOREIGN KEY (act_id) REFERENCES actors (act_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE
    )
"""

create_table_oscar_awarded = """
    DROP TABLE IF EXISTS 'oscar_awarded';
    CREATE TABLE 'oscar_awarded' (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER REFERENCES movie (mov_id) ON DELETE CASCADE
    )
"""


if __name__ == '__main__':
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()

        cursor.executescript(create_table_director)
        cursor.executescript(create_table_movie)
        cursor.executescript(create_table_movie_director)
        cursor.executescript(create_table_actors)
        cursor.executescript(create_table_movie_cast)
        cursor.executescript(create_table_oscar_awarded)

        cursor.execute(cmd_sql.insert_table_movie)