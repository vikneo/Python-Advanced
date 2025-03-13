import random
import sqlite3
import os
import logging.config
import datetime

from utilits.logging.log_conf import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

update_new_schedule_sql = """
INSERT INTO table_friendship_schedule (employee_id, date) VALUES (?, ?)
"""


def get_a_sport(cur: sqlite3.Cursor) -> list:
    new_list_sports = []
    sports = cur.execute("""SELECT DISTINCT preferable_sport FROM 'table_friendship_employees' """).fetchall()
    logger.info('A list of all sports has been received')
    [new_list_sports.append((i, sport[0])) for i, sport in enumerate(sports)]

    return new_list_sports


def get_working_days(cur: sqlite3.Cursor) -> list:
    working_days = []
    result = cur.execute("""SELECT employee_id, date FROM 'table_friendship_schedule'""").fetchall()
    logger.info('A list of all employees and dates has been received')
    for day in result:
        week = datetime.datetime.strptime(day[1], '%Y-%m-%d').weekday()
        logger.info("The day of the week is selected from the date")
        working_days.append((week, day[0], day[1]))
        logger.info("Added data to the array `working_days`")

    return working_days


def get_employees(cur: sqlite3.Cursor) -> list:
    data = cur.execute("""SELECT * FROM 'table_friendship_employees' """).fetchall()
    logger.info("A list of all employees and their sports sections was received")
    return data


def set_schedule(sports: list, working_days: list, employees: list = None):
    new_schedule = []
    for working_day in working_days:
        id_employee = working_day[1]
        week = working_day[0]
        logger.info("Comparison of the day of the section and the employee's hobby")
        if sports[week][1] == employees[id_employee - 1][2]:
            logger.info(f"`{sports[week][1]}` On this day, the employee `{employees[id_employee - 1][1]}` cannot work")
            while True:
                employee = random.choice(employees)
                logger.info('We change it to another employee')
                if sports[week][1] != employees[2]:
                    logger.info(f'The employee `{employees[1]}` has been replaced. Adding to the array `new_schedule`')
                    new_schedule.append((employee[0], working_day[2]))
                    break
        else:
            new_schedule.append((id_employee, working_day[2]))
            logger.info('Filling in the array for the new schedule')
    return new_schedule


def update_work_schedule(cur: sqlite3.Cursor) -> None:
    sports = get_a_sport(cur)
    work_days = get_working_days(cur)
    employees = get_employees(cur)
    new_schedule = set_schedule(sports, work_days, employees)
    logger.info(f"Updating the table `table_friendship_schedule` with a new schedule")
    cur.execute("""DELETE FROM 'table_friendship_schedule'""")
    cur.executemany(update_new_schedule_sql, new_schedule)


if __name__ == '__main__':
    with sqlite3.connect(path_to_db) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        get_working_days(cursor)
        update_work_schedule(cursor)
        conn.commit()
