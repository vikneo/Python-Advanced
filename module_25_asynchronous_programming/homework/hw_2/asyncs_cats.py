import asyncio
from datetime import datetime
import aiofiles
import aiohttp
import time

from config import URL, OUT_PATH_DIR, CATS_WE_WANT

today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


async def get_cat(client: aiohttp.ClientSession, idx: int) -> None:
    """
    Получает изображение из ссылки и передается в функцию запись в файл
    """
    async with client.get(URL) as response:
        result = await response.read()
        await write_to_disk(result, idx)


async def write_to_disk(content: bytes, _id: int):
    """
    Функция сохраняет изображение на диске
    """
    file_path = "{}/{}.png".format(OUT_PATH_DIR, _id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats(cats_we_want):
    """
    Получает количество ссылок, которое определенно в переменной `CATS_WE_WANT`
    """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout()) as client:
        tasks = [get_cat(client, i) for i in range(cats_we_want)]
        return await asyncio.gather(*tasks)


def main_asyncs(cats_we_want):
    """
    Режим асинхронности
    """
    start = time.time()
    asyncio.run(get_all_cats(cats_we_want))

    return {'data': today, 'func_name': main_asyncs.__name__, 'time': round(time.time() - start, 2)}


if __name__ == '__main__':
    print(main_asyncs(CATS_WE_WANT))
