import random
import sqlite3
import os
import logging.config

from utilits.logging.log_conf import dict_config
from action_to_db import database
from command_uefa import (
    teams_levels,
    select_command_by_level,
    insert_draw_data
    )

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

name_db = 'homework.db'
path_to_db = os.path.join(BASE_DIR, name_db)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


def generate_test_data(
        cur: sqlite3.Cursor,
        num_of_groups: int
) -> None:
    
    cur.execute("""DELETE FROM 'uefa_draw'""")
    logger.info("The cleaned table `uefa_draw` from of old records")

    logger.info("Let's start the draw")
    draw_data = []
    for num_group in range(1, num_of_groups + 1):
        logger.info(f"The formation of the group `{num_group}` has begun")
        levels = cur.execute(teams_levels)
        for num, level, *_ in enumerate(levels.fetchall()):
            logger.info("We get data on the level of the team")
            commands = cur.execute(select_command_by_level, level)
            list_num_commands = [i[0] for i in commands.fetchall()]
            logger.info("A list of team numbers by level has been received")
            if num == 1:
                draw_data.append((num_group, random.choice(list_num_commands)))
                logger.info(f"A team with the `{level}` level has been selected")
            draw_data.append((num_group, random.choice(list_num_commands)))
            logger.info(f"A team with the `{level}` level has been selected")

    logger.info("Writing the data to the table `uefa_draw`")
    database.insert(insert_draw_data, draw_data, 'uefa_draw')


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    database.create()
    generate_test_data(database.cursor, number_of_groups)
