from typing import Tuple, Any

import requests
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import logging.config
import time
import os

from module_11_multitasking.homework.hw2.created_db import DataBase
from utilits.logging.log_conf import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger('star_wars_v2')

BASE_DIR = os.path.dirname(__file__)
name_db = os.path.join(BASE_DIR, 'star_wars.db')
name_table = 'star_wars'
star_wars_db = DataBase(name_db, name_table)

base_url = "https://www.swapi.tech/api/people"


class StarWarsParserAPI:

    def __init__(self, url: str, deep: int = 2) -> None:
        self.url = url
        self.deep = deep

    def extractor_link(self) -> list:
        links = []
        response = requests.get(self.url).json()
        for i in range(self.deep):
            logger.warning(f"Парсим {i + 1}-ю страницу")
            for link in response['results']:
                links.append(link['url'])
                logger.info(f"Ссылка о персонаже `{link['name']}` - добавлена")
            if i < self.deep - 1:
                response = requests.get(response['next']).json()
                logger.warning("Переходим к следующей странице")

        return links

    @staticmethod
    def get_result(url: str) -> tuple[Any, Any, Any]:
        response = requests.get(url).json()

        data = response['result']['properties']
        result = (data['name'], data['gender'], data['birth_year'])
        return result

    @staticmethod
    def action(data):
        for url in data:
            star_wars_db.insert_data(url)


star_war = StarWarsParserAPI(base_url)


def pool_load():
    start = time.time()
    with mp.Pool(processes=mp.cpu_count()) as _pool:
        result = _pool.map(star_war.get_result, star_war.extractor_link())

    logger.warning(f'Pool closed in {time.time() - start} seconds')
    return result


def thread_pool_load():
    start = time.time()
    with ThreadPool(processes=mp.cpu_count()) as _pool:
        result = _pool.map(star_war.get_result, star_war.extractor_link())

    logger.warning(f'Thread pool closed in {time.time() - start} seconds')
    return result


if __name__ == '__main__':
    try:
        star_wars_db.created_base()
    except Exception as err:
        logger.exception(err)

    pool = pool_load()
    star_war.action(pool)

    thread_pool = thread_pool_load()
    star_war.action(thread_pool)
