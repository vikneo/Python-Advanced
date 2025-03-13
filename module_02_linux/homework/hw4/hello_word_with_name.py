"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

WEEKDAY = {
    0: 'Хорошего понедельника',
    1: "Хорошего вторника",
    2: "Хорошей среды",
    3: "Хорошего четверга",
    4: "Хорошей пятницы",
    5: "Хорошей субботы",
    6: "Хорошего воскресения"
}


@app.route('/hello-world/<name>')
def hello_world(name):
    _day = datetime.today().weekday()
    return f"И тебе привет {name}. {WEEKDAY[_day]}!"


if __name__ == '__main__':
    app.run(debug=True)
