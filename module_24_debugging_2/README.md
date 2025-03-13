# Основы дебаггинга и профилирования. Часть 2

@ Актуально на 02.03.2025

[Prometheus](https://prometheus.io/docs/prometheus/latest/) - оф. документация<br>
[Grafana](https://grafana.com/docs/grafana/latest/introduction/) - оф. документация<br>

## Мониторинг с Prometheus + Grafana

* [Что такое Prometheus?](#что-такое-prometheus)
* [Установка Prometheus для Flask](#установка-prometheus-для-flask-на-ubuntu-2204)
* [Метрики Prometheus](#метрики-prometheus)
* [Конфигурация Prometheus](config_prometheus.md)
* [Что такое Grafana?](grafana.md)
* [Конфигурация Docker](#конфигурация-docker)
* [Управление контенерами](#когда-все-подготовлено)

Структура приложения для **Примера**
```html
work_dir
    |
    |----app
    |     |----static
    |     |       |---css
    |     |----templates
    |     |       |---base
    |     |----app.py
    |     |----Dockerfile
    |     |----requirements.txt
    |----prometheus
    |       |---config.yml
    |----docker_compose.yaml
```

### Что такое Prometheus?

**Prometheus** — это набор инструментов с открытым исходным кодом, написанный на языке программирования *Golang* и представляющий собой полноценную систему мониторинга и оповещения.

Изначально продукт был создан SoundCloud, однако сейчас поддерживается сообществом разработчиков независимо от какой-либо компании.

Prometheus состоит из следующих компонентов:

* основной [сервер Prometheus](https://github.com/prometheus/prometheus), который собирает и хранит данные;
* [клиентские библиотеки](https://prometheus.io/docs/instrumenting/clientlibs/) для инструментирования кода приложения;
* [push-шлюз](https://github.com/prometheus/pushgateway) для поддержки недолговечных заданий;
* [экспортеры специального назначения](https://prometheus.io/docs/instrumenting/exporters/) для таких сервисов, как HAProxy, StatsD, Graphite и т. д.;
* [alertmanager](https://github.com/prometheus/alertmanager) для обработки оповещений

Все эти компоненты нужны для выполнения трех основных операций, на которых основывается Prometheus:

* Сбор. Опрашивать внешние службы, собирая данные для будущих метрик;
* Обработка. Выполнять правила, на основе которых обрабатываются полученные данные;
* Вывод. Сохранять полученные результаты в базу данных для последующей визуализации в виде метрик;
<hr>

Назад к [содержанию](#мониторинг-с-prometheus--grafana) ↑

### Установка Prometheus для Flask на Ubuntu-22.04

```html
pip install prometheus-flask-exporter
```

* Встроить Prometheus во Flask
```html
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
```
* Что бы увидеть метрики (по умолчанию) перейдите на endpoint ***/metrics***
```html
http://localhost:5000/metrics
```
<hr>

Назад к [содержанию](#мониторинг-с-prometheus--grafana) ↑

### Метрики Prometheus

* Назвав экземпляр PrometheusMetrics **metrics**, то с помощью его имени можно декорировать функции для сбора данных:
    * @metrics.counter(..);
    * @metrics.gauge(..);
    * @metrics.summary(..);
    * @metrics.histogram(..);

* Счетчики подсчитываю вызовы, а остальные собирают метрики в зависимости от продолжительности этих вызовов.

* Пример **@metrics.counter(..)**:
```html
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/page_one', methods=['GET'])
@metrics.counter(
        name='app_counter_page_one',
        description='Endpoint page_one',
        labels={'status': lambda resp: resp.status_code}
)
def page_one():
    return 'Page_one OK', 200
```
Посетив страницу *http://localhost:5000/page_one* приведет к увеличению счетчика

* Например, на странице *http://localhost:5000/metrics* из всех записей появится метрика в виде:
```html
...
app_counter_page_one{status="200"} 1
# где 1 - кол-во обращений к endpoin /page_one
...
```

* Вариант, где можно кастомизировать счетчик для нескольких endpoints
```html
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


custom_count = metrics.counter(
        name='app_counter_by_endpoint',
        description='Request by endpoints',
        labels={'status': lambda resp: resp.status_code,
                'path': lambda: request.path}
)


@app.route('/page_one', methods=['GET'])
@custom_count
def page_one():
    return 'Page_one OK', 200


@app.route('/page_two', methods=['GET'])
@custom_count
def page_two():
    return 'Page_two OK', 200
```

* Посмотрим на метрики *http://localhost:5000/metrics*, счетчик работает для наших двух endpoints

```html
...
app_counter_by_endpoint_total{path="/one",status="200"} 5.0
app_counter_by_endpoint_total{path="/two",status="200"} 9.0
...
```
Перейти к настройкам [Grafana](grafana.md)

<hr>

Назад к [содержанию](#мониторинг-с-prometheus--grafana) ↑

### Конфигурация Docker

* Создаем *Dockerfile* для нашего приложения в каталоге **app**
* Вносим изменения в файл
```html
FROM python:3-alpine

ADD requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r /tmp/requirements.txt

ADD app/ /var/server/

CMD python /var/server/app.py
```
 - Здесь:
    - Добавляем *requirements.txt* в католог /temp/ будущего контейнера;
    - Обновляем пакет **pip** и устанавливаем все зависимости;
    - Добавляем содержимое приложения **app/** в каталог /var/server/;
    - Запускаем приложение внутри контейнера;

* Создаем в корневом каталоге **work_dir** файл **docker-compose.yaml**
* Вносим изменения. 
```html
# что бы не было предупреждения, version можно закоментировать
# в новых версиях данная дирректива не требуется
# version: '2'

services:
    # Сборка и запуск нашего приложения
  app:
    build:
      context: app
    stop_signal: SIGKILL
    ports:
      - "5000:5000"

    # Подклчение сервиса сбора данных "Prometheus"
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus/config.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

    # Подключение визуализации мониторинга "Grafana"
  grafana:
    image: grafana/grafana:5.1.0
    ports:
      - "3000:3000"
```
Настройки Prometheus [здесь](config_prometheus.md)

Настройки Grafane [здесь](grafana.md)

<hr>

Назад к [содержанию](#мониторинг-с-prometheus--grafana) ↑

## Управление контенерами

### Когда все подготовлено !!!

* Собираем наш контейнер
```html
docker compose build app
```

* После сборки поднимаем наши конрейнеры
```html
docker compose up
```

* Остановить контейнер
    ```html
    docker compose stop
    ```
    ИЛИ
    ```html
    docker compose down -v
    ```
    Позволит остановить все контейнеры и удалить **(не образы)**

* Типа *убираем за собой* и образы тоже
```html
docker compose down -v --rmi all
```
<hr>

Назад к [содержанию](#мониторинг-с-prometheus--grafana) ↑