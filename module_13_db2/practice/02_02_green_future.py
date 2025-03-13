import sqlite3
import os
import logging.config

from config.logger import dict_config

BASE_DIR = os.path.dirname(__file__)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "practise.db"
path_to_db = os.path.join(BASE_DIR, name_db)

great_days = """
select count(action), (select count(distinct date) from table_green_future where date like ?)
from table_green_future
where date like ? and action like 'отнесли%'
"""


def get_number_of_lucky_days(c: sqlite3.connect, month_number: int) -> float:
    c.execute(great_days, (f"%-{month_number}-%", f"%-{month_number}-%"))
    count_great_day, days_mount = c.fetchall()[0]
    logger.info(f"Кол-во удачный дней {count_great_day}, и дней в месяце: {days_mount}")
    percentage_great_days = (count_great_day / days_mount) * 100
    logger.info(f"Процент удачных дней в данном месяце: {percentage_great_days} %")
    return percentage_great_days


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
        logger.info(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
