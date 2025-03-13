import sqlite3
import os
import logging.config

from config.logger import dict_config

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)


sql_script_to_execute = " \
UPDATE table_russian_post as post \
    SET order_day = replace(post.order_day, '-05-', '-06-') \
    WHERE order_day LIKE '%-05-%'; \
    " 

if __name__ == "__main__":
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script_to_execute)
        conn.commit()
