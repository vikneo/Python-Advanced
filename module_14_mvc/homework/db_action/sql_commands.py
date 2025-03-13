"""
The module allows you to store SQL commands for a database
"""

sql_exists = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """

sql_create_table = """CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER default 0
            )"""

sql_create = """
        INSERT INTO `table_books` (title, author) VALUES (?, ?)
        """

sql_update_views = """ UPDATE `table_books` SET views=views + 1"""
sql_update_view = """ UPDATE `table_books` SET views=views + 1 WHERE id=? """

sql_delete = """DELETE FROM `table_books` WHERE id=?"""

sql_select_all = """ SELECT * FROM `table_books` """

sql_select_filter = """SELECT * FROM `table_books` WHERE author LIKE ?"""

sql_select_get = """SELECT * FROM `table_books` WHERE id=?"""
