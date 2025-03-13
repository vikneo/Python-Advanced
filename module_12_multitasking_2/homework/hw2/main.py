import subprocess
import logging.config

from utilits.logging.log_conf import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


def process_count(username: str) -> int:
    command = f"ps -u {username} -o pid".split()
    response = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    logger.info(f"Получен список запущенных процессов от пользователя {username}")
    return len(response.stdout.read().splitlines()[1:])


def total_memory_usage(root_pid: int) -> float:
    command = f"ps --ppid {root_pid} -o %mem=".split()
    response = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    logger.info(f"Получен список древа процессов от `{root_pid}`")
    total_mem = [float(i) for i in response.stdout.read().splitlines()]
    logger.info(f"Подсчитано суммарное потребление памяти от `{root_pid}`")
    return sum(total_mem)


if __name__ == '__main__':
    user_name = 'vikneo'
    count_pid = process_count(user_name)
    logger.info(f"Кол-во запущенных процессов от `{user_name}` - {count_pid}")

    pid_root = 1
    total_memory = total_memory_usage(pid_root)
    logger.info(f"Суммарное потребление памяти древа процессов с корнем `{pid_root}` - {total_memory} %")
