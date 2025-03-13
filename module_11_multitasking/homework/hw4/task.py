import threading
import logging.config

from log_conf import dict_config


logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


class Task(threading.Thread):
    """
    The class generates tasks
    """
    def __init__(self, task, priority, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.task = task
        self.priority = priority
        logger.info(f"Task ({self.task}) - generated.")

    def __post_init__(self) -> None:
        """
        Для поддержки сортировки задач
        """
        self.sort_index = self.priority
