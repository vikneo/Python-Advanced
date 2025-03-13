import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 180
REMAINING_TICKETS: int = 10

logging.basicConfig(level = logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Director(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.semaphore: threading.Semaphore = semaphore
        logger.info("Director started print tickets")

    def run(self):
        global REMAINING_TICKETS, TOTAL_TICKETS
        while TOTAL_TICKETS:
            if REMAINING_TICKETS < 5:
                with self.semaphore:
                    print_tickets = 10 - REMAINING_TICKETS % 10
                    if print_tickets > TOTAL_TICKETS:
                        print_tickets = TOTAL_TICKETS
                    REMAINING_TICKETS += print_tickets
                    TOTAL_TICKETS -= print_tickets
                    logger.info(f"Director put {print_tickets} tickets")
        logger.info("Director stopped")


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global REMAINING_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if REMAINING_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                REMAINING_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {REMAINING_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    @staticmethod
    def random_sleep() -> None:
        if TOTAL_TICKETS <= 10:
            time.sleep(random.randint(3, 10))
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore(2)
    director = Director(semaphore=semaphore)
    director.start()

    sellers: List[Seller] = [director]
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
