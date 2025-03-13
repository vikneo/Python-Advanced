from datetime import datetime
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import threading
import requests
import time

from config import URL, OUT_PATH_DIR, CATS_WE_WANT

today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def write_to_disk(content: bytes, id: int) -> None:
    """
    Функция сохраняет изображение на диске
    """
    file_path = "{}/{}.png".format(OUT_PATH_DIR, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


def get_cats(link: str, idx: int):
    """
    Получает изображение из ссылки и передается в функцию запись в файл
    """
    with requests.get(link) as file:
        cat = file.content
        write_to_disk(cat, idx)


def main_threads(cats_we_want: int, threadpool: bool = True):
    """
    Варианты режимов многопоточности
    если threadpool = True (значение по умолчанию) используется multiprocessing.pool.ThreadPool(),
    если установить значение threadpool = False, тогда используется режим с threading.Thread()
    """
    start = time.time()
    if threadpool:
        with ThreadPool(processes=10) as pool:
            pool.starmap(get_cats, [(URL, _id) for _id in range(cats_we_want)])
    else:
        threads = [threading.Thread(target=get_cats, args=(URL, _id), daemon=True) for _id in range(cats_we_want)]
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

    return {'data': today, 'func_name': main_threads.__name__, 'time': round(time.time() - start, 2)}


if __name__ == '__main__':
    print(main_threads(CATS_WE_WANT))
    print(main_threads(CATS_WE_WANT, threadpool=False))
