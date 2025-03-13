import json
from flask import Flask, request, render_template


app = Flask(__name__)
messages = []


@app.route("/log", methods=["POST"])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    form = request.form
    messages.append(f'{form["levelname"]} | {form["name"]} | {form["lineno"]} | {form["msg"]}')

    return "logs pull [OK];", 200


@app.route("/logs", methods=["GET"])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    return render_template("log_detail.html", messages=messages, title="Logger")


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
