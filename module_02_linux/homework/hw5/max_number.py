"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:num_list>")
def max_number(num_list: str) -> str:
    number = [int(i) for i in num_list.split("/")]
    return f"Максимальное переданное число: <b>{max(number)}</b>"


if __name__ == "__main__":
    app.run(debug=True)
