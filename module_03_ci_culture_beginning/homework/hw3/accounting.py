from datetime import datetime
from flask import Flask

app = Flask(__name__)

TODAY = datetime.today().strftime("%Y %m %d")

storage = {}


def check_corrected_date(date: str) -> bool:
    """
    Функция проверяет на корректность введенной даты, что бы дата не была в будущем.
    :param data: str подается строка в формате YYYYMM.
    :return: Возвращает True, если введенная дата верна
    """
    try:
        year = int(date[:4])  # yaer = res[0]
        month = int(date[4:6])  # month = res[1]

        _year, _month, _day = TODAY.split()
        if year > int(_year) and month > int(_month):
            raise ValueError
        return True
    except Exception:
        raise ValueError


def go_by_month(month: int, year: int) -> int:
    """
    Подсчет накоплений за месяц или год
    :param month: int месяц.
    :param year: int год.
    :return: int общая сумма накоплений.
    """
    exp = 0
    if check_corrected_date(date=str(year) + str(month)):
        for money in storage[year][month]:
            exp += int(money)
        return exp


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int) -> str:
    """
    Добавление в словарь года, месяца и накопления в течение месяца.
    :param date: str дата в формате YYYYMMDD.
    :param number: int сумма которую нужно внести.
    :return: str (заполненный словарь)
    """
    # import re
    # pat = re.findall(r'[./-]', date)
    # res = date.split(pat[0])  ## На случай если дата будет вводится через символы (./-)
    try:
        if check_corrected_date(date=date):
            year = int(date[:4])  # yaer = res[0]
            month = int(date[4:6])  # month = res[1]
            storage.setdefault(year, {}).setdefault(month, [])
            storage[year][month].append(number)
            return f"{year} год, {month}-й месяц ({number} руб.) накопления внесены"
    except Exception:
        return "Введены не корректные данные. Проверьте правильность введенной даты!"

@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> str:
    """
    Функция принимает на вход год и выводит общую сумму накоплений за год.
    :param year: int год.
    :return: str результат общих накоплений за год.
    """
    exp = 0

    try:
        for mount in storage.get(year):
            exp += go_by_month(month=mount, year=year)
        return f"Накопления за {year} год: ({exp} руб.)"
    except TypeError:
        return f"В базе накоплений не существует {year} года."
    except IOError:
        return "Введены не корректные данные. Проверьте год!"
    except Exception:
        return f"В {year} году накопления составляют: ({exp} руб.)"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    """
    Функция принимает на вход числа в виде (год, месяц) для подсчета суммы накоплений.
    :param year: int год.
    :param month: int месяц.
    :return: str результат общих накоплений за месяц
    """
    exp = 0

    try:
        money = go_by_month(month=month, year=year)
        exp += money
        return f"Накопления в {year} году за {month}-й месяц: ({exp} руб.)"
    except IOError:
        return "Введены не корректные данные. Проверьте год и месяц!"
    except Exception:
        return f"Накоплений не было."


if __name__ == "__main__":
    app.run(debug=True)
