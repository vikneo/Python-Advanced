from pathlib import Path
from bs4 import BeautifulSoup
import logging.config

import asyncio
import aiofiles
import aiohttp

from config_log import config_dict


OUT_PATH = Path(__file__).parent
OUT_PATH_DIR = OUT_PATH
OUT_PATH_DIR.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
TIME_OUT = 100
DEPTH = 3

logging.config.dictConfig(config_dict)
logger: logging.Logger = logging.getLogger(__name__)

URL = ['https://rutube.ru']


async def extractor_links(data: list) -> list:
    """
    На вход подаются все ссылки из тега <a "href="> </a> с атрибутом "href" и
    извлекается ссылки, которые начинаются с "http".

    Возвращается отформатированный список ссылок.
    """
    list_links = []
    if data:
        logger.info("Получен список ссылок для экстрактора")
        for link in data:
            try:
                if link.get('href').startswith('http'):
                    list_links.append(link.get('href'))
            except Exception as err:
                logger.error(err)
        logger.info("Возвращаем список отформатированных ссылок")

    logger.warning("Полученный список - пуст")
    return list_links


async def write_to_file(link: str):
    """
    Записывает переданною ссылку в файл `links.txt`.
    """
    report = '{}/links.txt'.format(OUT_PATH)
    async with aiofiles.open(report, 'a') as file:
        logger.info(f'Отправлена ссылка для записи: {link}')
        await file.write(f"{link}\n")


async def get_url(client: aiohttp.ClientSession, url: str, depth: int):
    """
    Сканируется страница и данные передаются в `extractor_links()`,
    после в цикле отформатированные ссылки передаются в `write_to_file()` для записи в файл.

    При установленном значении глубины `depth` происходит погружение в полученные ссылки
    для дальнейшего сканирование рекурсивным методом
    """
    try:
        async with client.get(url) as response:
            result = await response.read()
            soup = BeautifulSoup(result, 'html.parser')
            links = await extractor_links(data = soup.find_all('a'))
            logger.info("Получен список ссылок")
            if links:
                for link in links:
                    await write_to_file(link)

            depth -= 1
            while depth:
                logger.info("Погружаемся на следующий уровень ссылок")
                tasks = [get_url(client, url, depth) for url in links]
                return await asyncio.gather(*tasks)
    except aiohttp.client_exceptions.ClientConnectionError as error:
        logger.error(f"Соединение по адресу {url} - закрылось")


async def action():
    try:
        connector = aiohttp.TCPConnector(limit_per_host=20, ssl = False, force_close = True)
        async with aiohttp.ClientSession(
                connector = connector,
                timeout = aiohttp.ClientTimeout(total = TIME_OUT),
                max_line_size = 8190 * 2,
                max_field_size = 8190 * 2
        ) as client:
            tasks = [get_url(client, url, DEPTH) for url in URL]
            return await asyncio.gather(*tasks)
    except TimeoutError as error:
        logger.warning(f"TIME_OUT - `{error}`")
    except Exception as err:
        logger.warning(f"ERROR - `{err}`")


def main():
    asyncio.run(action())
    logger.info("Все ссылки записаны в файл `links.txt`")


if __name__ == '__main__':
    main()
