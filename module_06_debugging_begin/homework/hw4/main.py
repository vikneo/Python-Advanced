"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
import shlex
from collections import defaultdict
from typing import Dict
import subprocess


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    counter_level = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    for key, _ in counter_level.items():
        cmd = f"""grep -c '{key}' skillbox_json_messages.log """
        cmd_list = shlex.split(cmd)
        count = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, close_fds=False)
        counter_level[key] = int(count.stdout.read().decode())

    return counter_level


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    hour = [f"0{str(hour)}" if len(str(hour)) < 2 else str(hour) for hour in range(0, 24)]
    dict_total_log_hours = {}
    for hour in hour:
        cmd = f"""grep -c '"time": "\<{hour}' skillbox_json_messages.log """
        cmd_list = shlex.split(cmd)
        count = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, close_fds=False)
        total_log = int(count.stdout.read().decode())
        dict_total_log_hours[hour] = total_log

    return int(max(dict_total_log_hours, key=dict_total_log_hours.get))


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    cmd = f"""
    grep -E '"level": "CRITICAL' skillbox_json_messages.log | 
    grep -E '"time": "(05:([0-1][0-9]):[0-5][0-9])"' | wc -l
    """
    counter_logs = int(subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode())
    return counter_logs


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    cmd = """grep -E '"message": .+doc' skillbox_json_messages.log | wc -l"""
    count_mes = int(subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode())
    return count_mes


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    warning_mes = []
    counter_worlds_dict = defaultdict(int)

    for level in data_file:
        if level["level"] == "WARNING":
            warning_mes.append(level["message"])

    for mes in warning_mes:
        for world in mes.split():
            counter_worlds_dict[world] += 1

    return max(counter_worlds_dict, key=counter_worlds_dict.get)


if __name__ == '__main__':
    data_file = []
    tasks = (task1, task2, task3, task4, task5)
    with open("skillbox_json_messages.log", 'r') as file:
        for line in file.readlines():
            data_file.append(json.loads(line.strip()))

    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
