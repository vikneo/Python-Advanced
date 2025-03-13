import logging
import logging.config
import os
from threading import Thread
from multiprocessing import Queue
import time

import requests

try:
    from utilits.logging.log_conf import dict_config
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger("module_12_server")
except ImportError:
    """
    Для VSCode (не корректно вызывается import )
    """
    BASE_DIR = os.path.dirname(__file__)
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename=os.path.join(BASE_DIR, 'server.log'),
        filemode='a',
        format='%(threadName)s - %(message)s',
        level=logging.INFO,
    )

base_url = 'http://127.0.0.1:8080/timestamp/'


def get_timestamp(queue):
    for _ in range(20):
        timestamp = time.time()
        response = requests.get(base_url + str(timestamp))
        if response.status_code == 200:
            result = response.text
            queue.put((timestamp, result))
            time.sleep(1)


def main():
    my_queue = Queue()
    start_time = time.time()
    threads = [Thread(target=get_timestamp, args=(my_queue,)) for _ in range(10)]
    for thread in threads:
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()

    while not my_queue.empty():
        _timestamp, _result = my_queue.get()
        logger.info(f"{_timestamp} {_result}")

    my_queue.close()

    logger.info(f"Work generate loggers stopping {time.time() - start_time} sec")


if __name__ == '__main__':
    main()
