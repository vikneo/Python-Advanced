from datetime import datetime
import multiprocessing as mp
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


def main_processes(cats_we_want, queue: bool = False):
    """
    Режим многопроцессорности
    """
    start = time.time()
    if not queue:
        processes = [mp.Process(target=get_cats, args=(URL, idx)) for idx in range(cats_we_want)]

        for proc in processes:
            proc.start()
        for proc in processes:
            proc.join()
    else:
        _queue = mp.Queue()
        _pool = mp.Pool(processes=mp.cpu_count())

        for i in range(cats_we_want):
            _queue.put(get_cats(URL, i))
        
        _queue.close()
        _queue.join_thread()

        _pool.close()
        _pool.join()

    return {'data': today, 'func_name': main_processes.__name__, 'time': round(time.time() - start, 2)}


if __name__ == '__main__':
    print(main_processes(CATS_WE_WANT))
    # print(main_processes(10, queue=True))
