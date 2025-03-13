import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"


def var_1():
    CREATE_USER_TABLE = """
    DROP TABLE IF EXISTS 'user';
    CREATE TABLE 'user' (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        email TEXT VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL
    ) 
    """

    CREATE_POST_TABLE = """
    DROP TABLE IF EXISTS 'post';
    CREATE TABLE 'post' (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author VARCHAR(255) NOT NULL REFERENCES user (user_id) ON DELETE CASCADE,
        content TEXT NOT NULL DEFAULT ''
    );
    """

    CREATE_TABLE_LIKE = """
    DROP TABLE IF EXISTS 'like';
    CREATE TABLE 'like' (
        like_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES user (user_id) ON DELETE CASCADE,
        post_id INTEGER NOT NULL,
        FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE 
    )
    """
    return CREATE_USER_TABLE, CREATE_POST_TABLE, CREATE_TABLE_LIKE


def var_2():
    CREATE_USER_TABLE = """
    DROP TABLE IF EXISTS 'user';
    CREATE TABLE 'user' (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        email TEXT VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL
    ) 
    """

    CREATE_POST_TABLE = """
    DROP TABLE IF EXISTS 'post';
    CREATE TABLE 'post' (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author VARCHAR(255) NOT NULL,
        content TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (author) REFERENCES user (username) ON DELETE CASCADE
    );
    """

    CREATE_TABLE_LIKE = """
    DROP TABLE IF EXISTS 'like';
    CREATE TABLE 'like' (
        like_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES user (user_id) ON DELETE CASCADE,
        post_id INTEGER NOT NULL,
        FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE 
    )
    """
    return CREATE_USER_TABLE, CREATE_POST_TABLE, CREATE_TABLE_LIKE


def create_tables() -> None:
    with sqlite3.connect("surrogate.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(ENABLE_FOREIGN_KEY)
        # variant_1 = var_1()
        variant_1 = var_2()
        cursor.executescript(variant_1[0])
        cursor.executescript(variant_1[1])
        cursor.executescript(variant_1[2])


if __name__ == '__main__':
    create_tables()