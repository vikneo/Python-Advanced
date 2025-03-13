import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config
from decorators.decorators import time_tracker

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

file_name_wrong_fees_csv = 'wrong_fees.csv'
path_to_file = os.path.join(BASE_DIR, file_name_wrong_fees_csv)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

DELETED_WRONG_FEES = """DELETE FROM 'table_fees' WHERE truck_number=? AND timestamp=?"""


@time_tracker
def delete_wrong_fees(
        cur: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    try:
        with open(wrong_fees_file, 'r') as file:
            logger.info(f'Data read from {file_name_wrong_fees_csv}')
            for line in file.readlines()[1:]:
                data = line.replace('\n', '').split(',')
                cur.execute(DELETED_WRONG_FEES, data)
                logger.info(f'Automobile with number {data[0]} delete from base')
            logger.info('Wrong fees deleted from db')
    except FileNotFoundError:
        logger.error(f'File {wrong_fees_file} not found')


if __name__ == "__main__":
    with sqlite3.connect(path_to_db) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, path_to_file)
        conn.commit()
        logger.info('The data has been updated. Saving changes to the database')
