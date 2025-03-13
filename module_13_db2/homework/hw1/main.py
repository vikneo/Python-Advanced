import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


def check_if_vaccine_has_spoiled(
        cur: sqlite3.Cursor,
        truck_num: str
) -> bool:
    if not truck_num:
        logger.warning(f'Truck with number {truck_number if truck_number else "`?`"} not exists')
        return False
    cur.execute(
        """
        SELECT EXISTS (SELECT * FROM 'table_truck_with_vaccine' WHERE truck_number = ?
        AND temperature_in_celsius NOT BETWEEN ? AND ?)
        """, (truck_num, 16, 20)
    )
    result = cur.fetchone()
    logger.info('Found truck witch number {}'.format(truck_num))
    return result[0]


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect(path_to_db) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        logger.info(
            f"The vaccine is {'not ' if not spoiled else ''}spoiled in "
            f"the truck with the number {truck_number if truck_number else '`?`'}")
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
