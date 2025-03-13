"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
import shlex
import signal
import subprocess
from typing import List

from flask import Flask


app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []

    get_port = shlex.split(f'lsof -i :{port}')
    res = subprocess.Popen(get_port, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    process = res.stdout.read().splitlines()[1:]

    for _port in process:
        pids.append(int(_port.split()[1]))

    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт.
    @param port: Порт
    """
    pids: List[int] = get_pids(port)
    if pids:
        for process in pids:
            cmd_kill = shlex.split(f'kill -{signal.SIGKILL} {process}')
            res = subprocess.run(cmd_kill, capture_output=True)
            if res.returncode == 0:
                print(f"\nСообщение системы '{app.name}': Порт {port} успешно освобожден!", end='')
                print(f"\nПроизводится автоматический запуск '{app.name}'на порту {port} ...")
                run(port)


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: Порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(3000)
    # run(5000)
