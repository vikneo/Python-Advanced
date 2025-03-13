from random import random
import time

from flask import Flask, render_template
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/index', methods = ['GET'])
@metrics.counter(name='doors_app_counter_index',
                 description = 'Endpoint `index`',
                 labels = {'status': lambda resp: resp.status_code})
def index():
    context = {
        "title": 'Module 24',
        'stag': 0,
    }
    return render_template('base/base.html', context = context, status_code = 200), 200


@app.route('/page_one', methods = ['GET'])
@metrics.counter(name='doors_app_counter_page_one',
                 description = 'Endpoint `page_one`',
                 labels = {'status': lambda resp: resp.status_code})
def page_one():
    context = {
        "title": 'Страничка №1',
        'stag': 1,
    }
    return render_template('page_one.html', context = context, status_code = 200), 200


@app.route('/page_two', methods = ['GET'])
@metrics.counter(name='doors_app_counter_page_two',
                 description = 'Endpoint `page_two`',
                 labels = {'status': lambda resp: resp.status_code})
def page_two():
    context = {
        "title": 'Страничка №2',
        'stag': 2,
    }
    rand_num = random()
    if rand_num > 0.75:
        if rand_num > 0.83:
            raise ZeroDivisionError("Что то поделили на ноль")
        time.sleep(2)
        return render_template('page_two.html', context = context, status_code = 400), 400
    return render_template('page_two.html', context = context, status_code = 200), 200


@app.route('/page_three', methods = ['GET'])
@metrics.counter(name='doors_app_counter_page_three',
                 description = 'Endpoint `page_three`',
                 labels = {'status': lambda resp: resp.status_code})
def page_three():
    context = {
        "title": 'Страничка №3',
        'stag': 3,
    }
    rand_num = random()
    if rand_num > 0.25:
        if 0.73 < rand_num < 0.83:
            raise TypeError("Зло вырвалось наружу")
        time.sleep(4)
        return render_template('page_three.html', context = context, status_code = 400), 400
    return render_template('page_three.html', context = context, status_code = 200), 200


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, threaded=True)