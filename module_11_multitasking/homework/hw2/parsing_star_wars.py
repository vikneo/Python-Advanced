import requests
import threading
import logging.config
import time
import os

from created_db import DataBase
from utilits.logging.log_conf import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(__file__)
name_db = os.path.join(BASE_DIR, 'star_wars.db')
name_table = 'star_wars'
star_wars_db = DataBase(name_db, name_table)


class ParsingApiStarWars(threading.Thread):
    """
    Парсинг сайта API Star Wars в многопоточном режиме с помощью модуля "threading"

    base_url = "https://www.swapi.tech/api/"
    Настраиваемы параметры:
    deep - количество посещаемых страниц сайта
    # limit - отображение количества записей на странице //

    Доступные аттрибуты:
    films Строка-- корневой URL-адрес ресурсов фильма
    people Строка-- корневой URL для ресурсов People
    planets Строка-- корневой URL для ресурсов планеты
    species Строка-- корневой URL для ресурсов вида
    starships Строка-- корневой URL-адрес ресурсов Starships
    vehicles Строка-- корневой URL для ресурсов транспортных средств
    """

    def __init__(self, url: str, multiple: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multiple = multiple
        self.base_url = url
        self.deep = 2
        self.links = []

    @staticmethod
    def insert_date_to_db(data: dict) -> None:
        result = data['result']['properties']
        _data = (result['name'], result['gender'], result['birth_year'])
        star_wars_db.insert_data(data = _data)

    @staticmethod
    def _get_url(url: str):
        res = requests.get(url).json()
        return res

    def link_extractor(self) -> list:
        if not self.links:
            response = self._get_url(self.base_url)
            for i in range(self.deep):
                logger.info(f"Парсим {i + 1}-ю страницу")
                for link in response['results']:
                    self.links.append(link['url'])
                    logger.info(f"Ссылка о персонаже `{link['name']}` - добавлена")
                if i < self.deep:
                    response = self._get_url(response['next'])
                    logger.info("Переходим к следующей странице")

        return self.links

    def run(self):
        if not self.multiple:
            for link in self.links:
                self.insert_date_to_db(self._get_url(link))
        else:
            self.insert_date_to_db(self._get_url(self.base_url))


def format_print(data: list) -> None:
    length = 25
    print(f"+{'':-^8}+{'':-^{length}}+{'':-^15}+{'':-^{length}}+")
    print(f"|{'ID':^8}|{'Имя':^{length}}|{'Пол':^15}|{'Дата рождения':^{length}}|")
    print(f"+{'':-^8}+{'':-^{length}}+{'':-^15}+{'':-^{length}}+")
    for people in data:
        print(f"|{people[0]:^8}|{people[1]:^{length}}|{people[2]:^15}|{people[3]:^{length}}|")
    print(f"+{'':-^8}+{'':-^{length}}+{'':-^15}+{'':-^{length}}+")


base_url = "https://www.swapi.tech/api/people"


def main():
    start = time.time()
    people = ParsingApiStarWars(url = base_url)
    people.link_extractor()
    people.run()
    format_print(star_wars_db.select_data())
    logger.warning(f"{main.__qualname__} - took {round(time.time() - start, 4):.2f} seconds")


def maim_multiple():
    start = time.time()
    pages = []
    request = requests.get(base_url).json()
    pages.extend(request['results'])
    request = requests.get(request['next']).json()
    pages.extend(request['results'])

    peoples = [ParsingApiStarWars(url = link['url'], multiple = True) for link in pages]
    for people in peoples:
        people.start()
    for people in peoples:
        people.join()

    format_print(star_wars_db.select_data())
    logger.warning(f"{maim_multiple.__qualname__} - took {round(time.time() - start, 4):.2f} seconds")


if __name__ == '__main__':
    try:
        star_wars_db.created_base()
    except Exception as e:
        logger.exception(e)

    while True:
        answer = input("\nВыбрать режим парсинга\n"
                       "1 - синхронный режим\n"
                       "2 - асинхронный режим\n"
                       "Ваш выбор: ")
        if answer == "1":
            main()
            break
        if answer == "2":
            maim_multiple()
            break
        print("Попробуйте еще раз")
