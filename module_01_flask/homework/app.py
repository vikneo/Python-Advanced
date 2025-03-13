import datetime
import random
import re
from random import choice
from flask import Flask
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

app = Flask(__name__)

list_cars = ['Toyota Camry', 'Renault', 'Chevrolet', 'Ford', 'Lada']
list_cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
result = []
visits = 0


@app.route('/hello_world')
def hello_world():
    return 'Привет Мир!!!'


@app.route('/cars')
def cars():
    return ", ".join(list_cars)


@app.route('/cats')
def cats():
    return choice(list_cats)


@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def get_time_future():
    current_time = datetime.datetime.now()
    current_time_future = datetime.timedelta(hours=1)
    current_time_future += current_time
    return f'Время через час составит: {current_time_future}'


@app.route('/get_random_word')
def get_random_word():
    if not result:
        with open(BOOK_FILE, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                search_randon_work(res=line)

    return f'Случайное слово из повести "Война и мир": << {random.choice(random.choice(result))} >>'


def search_randon_work(res):
    if res.strip():
        resp = re.findall(r'\b\w+', res)
        result.append(resp)


@app.route('/counter')
def counter():
    global visits
    visits += 1
    return str(visits)


if __name__ == "__main__":
    app.run(debug=True)
