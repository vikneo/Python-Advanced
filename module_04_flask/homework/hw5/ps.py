"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex
import subprocess
from typing import List
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args: List[str] = request.args.getlist("arg", type=str)
    cmd_str = f"ps {' '.join([shlex.quote(sym) for sym in args])}"
    cmd_list = shlex.split(cmd_str)

    result = subprocess.run(cmd_list, capture_output=True, shell=True)
    answer = result.stdout.decode()

    return f"<pre>{answer}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
