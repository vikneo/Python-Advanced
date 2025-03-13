"""
Напишите Flask POST endpoint /calculate,
который принимает на вход арифметическое выражение и
вычисляет его с помощью eval (о безопасности думать не нужно,
работайте только над фукнционалом).

Поскольку наш Flask endpoint работает с арифметическими выражениями,
напишите 4 error_handler-а, которые будет обрабатывать
ArithmeticError, ZeroDivisionError, FloatingPointError и OverflowError
(о значении этих исключений вы можете посмотреть
вот на этой страничке https://docs.python.org/3/library/exceptions.html ).

Напишите по unit-тесту на каждую ошибку: тест должен проверять, что ошибка обрабатывается

Примечание: рекомендуется обрабатывать ArithmeticError,
перехватывая InternalServerError,
остальные классы ошибок можно обрабатывать напрямую.
"""
from typing import Optional

from werkzeug.exceptions import InternalServerError

from flask import Flask

app = Flask(__name__)


@app.route('/calculate/<path:expression>')
def calculate(expression: str) -> str:

    return f"{expression} = {eval(expression)}"


@app.errorhandler(InternalServerError)
def handler_exception_arithmetic(error: InternalServerError) -> str | tuple[str, int]:
    original: Optional[Exception] = getattr(error, "original_exception", None)

    if isinstance(original, ArithmeticError):
        return f"Арифметические действия! Описание: - тип {original}; - ошибка {error}", 400
    

@app.errorhandler(ZeroDivisionError)
def handler_exception(error: ZeroDivisionError):
    return f"На ноль делить нельзя! Описание: - {error}", 400


@app.errorhandler(FloatingPointError)
def handler_exception(error: FloatingPointError):
    return f"Не верная операция с типом float! Описание: - {error}", 400


@app.errorhandler(OverflowError)
def handler_exception(error: OverflowError):
    return f"Не хватает выделенной памяти для вычисления! Описание: - {error}", 400


@app.errorhandler(SyntaxError)
def handler_exception(error: SyntaxError):
    return f"При выполнении операции допущена синтаксическая! Описание: - {error}", 400


@app.errorhandler(NameError)
def handler_exception(error: NameError):
    return f"Вычисления должны выполняться только с цифрами! Описание: - {error}", 400


if __name__ == '__main__':
    app.run(debug=True)
