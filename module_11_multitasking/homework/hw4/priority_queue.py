import random
import queue
import threading
import logging.config
import time

from task import Task
from log_conf import dict_config

TASKS = [Task(task = f'task_name_{i}', priority = random.randint(1, 100)) for i in range(10)]

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    """
    The class adds task with priority queue.
    """
    def __init__(self, catcher: queue.PriorityQueue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.catcher = catcher
        logger.info("Producer thread started")

    def run(self):
        for i, task in enumerate(TASKS):
            self.catcher.put((task.priority, task))
            logger.info(f"Production flow, adds task {i} with priority {task.priority}")


class Consumer(threading.Thread):
    """
    The class running task with priority queue.
    """
    def __init__(self, catcher: queue.PriorityQueue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.catcher = catcher

    def run(self):
        logger.info("Consumer thread started")
        while True:
            try:
                start = time.time()
                priority, task = self.catcher.get(timeout = 1)

                random_sleep()
                logger.info(
                    f"Consumer flow, running task {task.task} with priority {task.priority}."
                    f"{' ' * 10} sleeping ({time.time() - start}) s.")
                self.catcher.task_done()
            except queue.Empty:
                logger.info(f"Consumer - queue empty. All tasks are completed")
                break
            except Exception as err:
                logger.exception(err)
                continue


def random_sleep() -> None:
    sec = random.random()
    time.sleep(sec)


def main():
    catcher = queue.PriorityQueue(10)
    producer = Producer(catcher)
    customer = Consumer(catcher)
    producer.start()
    customer.start()
    producer.join()
    customer.join()


if __name__ == '__main__':
    main()
