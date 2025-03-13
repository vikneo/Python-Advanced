## Конфигурация Prometheus

Основным файлом конфигурации в Prometheus является ***prometheus.yml*** — в нем прописываются настройки объектов мониторинга, периодичность сбора данных, условия для системы уведомлений, а также методы обработки и хранения информации.

* Файл конфигурации **prometheus/config.yml** для нашего приложения
```html
global:
  scrape_interval:     3s

  external_labels:
    monitor: 'app.py'


scrape_configs:
  - job_name: 'prometheus'

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'flask'

    dns_sd_configs:
      - names: ['app']
        port: 5000
        type: A
        refresh_interval: 5s
```

* Что бы запретить доступ к **endpoin /metrics**, можно отключить ее, передав **path=None**. Так же можно использовать start_http_server(port), чтобы открыть приложение на другом HTTP-порту, например **5099**.
```html
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app, path=None)

...

metrics.start_http_server(5099)
```


* В качестве альтернативы, вам нужно изменить ее путь от **/metrics** , для этого вы можете либо передать другой URI в качестве параметра пути **path**, либо использовать register_endpoint(..), чтобы установить это позже.

```html
metrics.register_endpoint('/new_path_for_metrics')
```

## Полезные ссылки

* [prometheus-flask-exporter README](https://github.com/rycus86/prometheus_flask_exporter/blob/master/README.md) - Использование, примеры и параметры конфигурации
* [Prometheus + Grafana](https://github.com/rycus86/prometheus_flask_exporter/tree/master/examples/sample-signals) - Пример посторение сигналов & app Flask
* [prometheus/client_python](https://github.com/prometheus/client_python) - Официальная клиентская библиотека Prometheus для Python
* [prometheus-flask-exporter on PyPI](https://pypi.org/project/prometheus-flask-exporter/) - Этот проект на PyPI
