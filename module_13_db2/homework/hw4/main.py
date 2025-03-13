import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

salary_ivan_sovin_sql = """SELECT salary FROM 'table_effective_manager' WHERE name LIKE 'Иван Совин'"""

salary_increase_sql = """
UPDATE 'table_effective_manager' 
    SET salary = ?
    WHERE name LIKE ? 
"""

get_salary_person_by_name_sql = """SELECT salary FROM 'table_effective_manager' WHERE name LIKE ?"""

employee_transfer_sql = """DELETE FROM 'table_effective_manager' WHERE name LIKE ?"""


def ivan_sovin_the_most_effective(
        cur: sqlite3.Cursor,
        person_name: str,
) -> None:
    """ Delete employee company if salary > Ivan Sovin or
    increase salary employee a 10% if salary < Ivan Sovin."""
    salary_sovin = get_salary_ivan_sovin(cur)
    old_salary = get_salary_by_name_employee(cur, person_name)
    new_salary = old_salary + (old_salary * 0.1)
    logger.info(f'The New salary of employee of the company is {new_salary}')

    if new_salary < salary_sovin:
        logger.info('The New salary of employee of the company is less than of Ivan Sovin')
        cur.execute(salary_increase_sql, (new_salary, "{}".format(person_name)))
        logger.info(f'The New salary of `{person_name}` is {new_salary}')
    else:
        logger.info('The New salary of employee of the company is higher than of Ivan Sovin')
        cur.execute(employee_transfer_sql, ("{}".format(person_name),))
        logger.info(f'Alas, you `{person_name}` are being transferred to another division')


def get_salary_ivan_sovin(cur: sqlite3.Cursor) -> int | float:
    """ Get salary of manager Ivan Sovin """
    cur.execute(salary_ivan_sovin_sql)
    _salary_sovin = cur.fetchone()[0]
    logger.info(f'The Salary Sovin is {_salary_sovin}')
    return _salary_sovin


def get_salary_by_name_employee(
        cur: sqlite3.Cursor,
        person_name: str,
):
    """ Get salary of employee company """
    cur.execute(get_salary_person_by_name_sql, ("{}".format(person_name),))
    _salary = cur.fetchone()[0]
    logger.info(f'The Old salary of employee of the company is {_salary}')
    return _salary


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect(path_to_db) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
        logger.info('The data has been updated. Saving changes to the database')
