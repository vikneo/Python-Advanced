import threading
import time
from typing import List
import requests

import logging

logging.basicConfig(level = logging.WARNING)


class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout = self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json = data, timeout = self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_book_by_id(self, book_id: int) -> dict:
        response = self.session.get(self.URL + f"/{book_id}", timeout = self.TIMEOUT)
        return response.json()

    def delete_book_by_id(self, book_id: int):
        response = self.session.delete(self.URL + f"/{book_id}", timeout = self.TIMEOUT)
        return response.status_code

    def patch_book_by_id(self, book_id: int, data: dict):
        response = self.session.patch(self.URL + f"/{book_id}", json = data, timeout = self.TIMEOUT)
        return response.json()

    def put_book_by_id(self, book_id: int, data: dict):
        response = self.session.put(self.URL + f"/{book_id}", json = data, timeout = self.TIMEOUT)
        return response.json()


class AuthorClient:
    URL: str = 'http://127.0.0.1:5000/api/authors'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_authors(self) -> dict:
        response = self.session.get(self.URL, timeout = self.TIMEOUT)
        return response.json()

    def add_new_author(self, data: dict):
        response = self.session.post(self.URL, json = data, timeout = self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_books_by_author_id(self, author_id: int) -> dict:
        response = self.session.get(self.URL + f"/{author_id}", timeout = self.TIMEOUT)
        return response.json()

    def delete_author_by_id(self, book_id: int):
        response = self.session.delete(self.URL + f"/{book_id}", timeout = self.TIMEOUT)
        return response.status_code


def time_tracker(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = round(time.time() - start, 4)
        logging.warning(f"'{func.__name__}' - {args[0].number}-st took {end:.6f} seconds")
        return result

    return wrapper


class AnalizAPI:
    """
    The class AnalizAPI sends requests to the "url" and the number is determined by the "number" variable,
    and session settings are also available, or the session is disabled
    and multithreading is enabled and disabled.

    :param number: (int) number of requests
    :param count_pool: (int) number of threads
    :return: None
    """
    def __init__(
            self,
            number: int,
            count_pool: int = 10,
    ) -> None:
        self.number = number
        self.count_pool = count_pool
        self.session = False
        self.multiple = True

    def set_session(self, session: bool) -> None:
        self.session = session

    def get_session(self) -> bool:
        return self.session

    def set_multiple(self, multiple: bool) -> None:
        self.multiple = multiple

    def get_multiple(self) -> bool:
        return self.multiple

    @time_tracker
    def counter_requests(self) -> None:
        for _ in range(self.number):
            if not self.get_session():
                client.get_all_books()
            else:
                client.session.get(client.URL)

    @time_tracker
    def counter_request_multiple(self) -> None:
        pools_list: List[threading.Thread] = []
        if self.get_multiple():
            for _ in range(self.number // self.count_pool):
                if not self.get_session():
                    pools = [threading.Thread(target = client.get_all_books) for _ in range(self.count_pool)]
                else:
                    pools = [threading.Thread(target = client.session.get, args = (client.URL,)) for _ in
                             range(self.count_pool)]
                for pool in pools:
                    pool.start()
                    pools_list.append(pool)

                for pool in pools:
                    pool.join()


if __name__ == '__main__':
    client = BookClient()
    test_request_10 = AnalizAPI(10)
    test_request_100 = AnalizAPI(100)
    test_request_1000 = AnalizAPI(1000)

    logging.warning("Request Counter:\n Session - OFF:\n Multiple - OFF:")
    test_request_10.counter_requests()
    test_request_100.counter_requests()
    test_request_1000.counter_requests()

    logging.warning("Request Counter: \nSession - OFF\nMultiple - ON:")
    test_request_10.counter_request_multiple()
    test_request_100.counter_request_multiple()
    test_request_1000.counter_request_multiple()

    logging.warning("Request Counter: \nSession - ON\nMultiple - OFF:")
    test_request_10.set_session(True)
    test_request_10.set_multiple(False)
    test_request_10.counter_requests()
    test_request_100.set_session(True)
    test_request_100.set_multiple(False)
    test_request_100.counter_requests()
    test_request_1000.set_session(True)
    test_request_1000.set_multiple(False)
    test_request_1000.counter_requests()

    logging.warning("Request Counter: \nSession - ON\nMultiple - ON:")
    test_request_10.set_multiple(True)
    test_request_10.counter_request_multiple()
    test_request_100.set_multiple(True)
    test_request_100.counter_request_multiple()
    test_request_1000.set_multiple(True)
    test_request_1000.counter_request_multiple()

    # client.session.post(
    #     client.URL,
    #     data=json.dumps({'title': '123', 'author': {"first_name": "ASD", "last_name": "Rfdghj", "middle_name": ''}}),
    #     headers={'content-type': 'application/json'}
    # )
