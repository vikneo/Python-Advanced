import sqlite3
import os


def conn_base(base_name):
    """Connects to the database and returns the cursor"""

    with sqlite3.connect(base_name) as conn:
        cursor = conn.cursor()
        return cursor
