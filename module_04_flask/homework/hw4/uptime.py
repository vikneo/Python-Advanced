"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
from flask import Flask

import os
import shlex
import subprocess

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    _UPTIME = os.popen("uptime -p").read()
    return f"Current uptime is {_UPTIME}"


@app.route("/uptime-v2", methods=['GET'])
def uptime_v2() -> str:
    cmd_str = "uptime -p"
    cmd = shlex.split(cmd_str)
    result = subprocess.run(cmd, capture_output=True)
    return f"Current uptime is {result.stdout.decode()}"


if __name__ == '__main__':
    app.run(debug=True)
