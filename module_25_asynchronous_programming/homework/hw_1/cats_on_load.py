import asyncio
from pathlib import Path

import aiohttp

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
TIME_OUT = 15


def write_to_disk(content: bytes, id: int) -> None:
    """
    Функция сохраняет изображение на диске
    """
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    """
    Асинхронный запуск функции write_to_disk для записи в файл на диск
    """
    async with client.get(URL) as response:
        print(f'Ответ сервера - {response.status}')
        result = await response.read()
        await asyncio.to_thread(write_to_disk, result, idx)


async def get_all_cats() -> aiohttp.client.ClientSession:
    """
    
    """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(TIME_OUT)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    try:
        res = asyncio.run(get_all_cats())
        print(f'Кол-во скаченных картинок - {len(res)}шт.')
    except asyncio.exceptions.TimeoutError:
        print(f'Время ожидания превысило установленное в {TIME_OUT}s')


if __name__ == '__main__':
    main()
