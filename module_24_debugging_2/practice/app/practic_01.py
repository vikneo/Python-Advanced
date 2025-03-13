import base64
import time
import random

from flask import Flask, render_template, request, url_for
from graphviz import Graph
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

custom_count = metrics.counter(
        name='app_counter_by_endpoint',
        description='Request by endpoints',
        labels={'status': lambda resp: resp.status_code,
                'path': lambda: request.path}
)


@app.route('/get-graph-image')
def get_graph_image():
    chart_data = Graph()

    chart_data.node('Idx', url_for('index'))
    chart_data.node('One', url_for('one'))
    chart_data.node('Two', url_for('two'))
    chart_data.node('Three', url_for('three'))
    chart_data.node('Err', url_for('error'))
    chart_data.edge('Idx', 'One')
    chart_data.edge('Idx', 'Two')
    chart_data.edge('Idx', 'Three')
    chart_data.edge('Idx', 'Err')

    chart_output = chart_data.pipe(format='png')
    chart_output = base64.b64encode(chart_output).decode('utf-8')

    return render_template('maps_points.html', chart_output=chart_output)


@app.route('/')
@custom_count
def index():
    time.sleep(random.random() * 0.2)
    return 'Hello World!', 200


@app.route('/one')
@custom_count
def one():
    time.sleep(random.random() * 0.2)
    return 'Hello page /one!', 200


@app.route('/two')
@custom_count
def two():
    time.sleep(random.random() * 0.4)
    return 'Hello page /two!', 200


@app.route('/three')
@custom_count
def three():
    time.sleep(random.random() * 0.6)
    return 'Hello page /three!', 400


@app.route('/error')
@custom_count
def error():
    time.sleep(random.random() * 0.8)
    return 'Oops!', 500


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, threaded=True)
