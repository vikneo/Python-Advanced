import operator
from flask import Flask
from flask_jsonrpc import JSONRPC

import logging.config

from config.log_config import dict_config

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "3.0",
            "method": "calc.add",
            "params": {"a": 7.8, "b": 5.3},
            "id": "1"
        }' http://localhost:5000/api

    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/2.2.2 Python/3.10.6
    Date: Fri, 09 Dec 2022 19:00:09 GMT
    Content-Type: application/json
    Content-Length: 54
    Connection: close

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": 13.1
    }
    """
    logger.debug(f"Let's sum up the numbers {a} and {b}")
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def sub(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
            -d '{
                "jsonrpc": "3.0",
                "method": "calc.sub",
                "params": {"a": 9.18, "b": 15.3},
                "id": "1"
            }' http://localhost:5000/api
    
    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.1.3 Python/3.10.11
    Date: Tue, 21 Jan 2025 02:14:06 GMT
    Content-Type: application/json
    Content-Length: 55
    Connection: close

    {
      "id": "1",
      "jsonrpc": "3.0",
      "result": -6.120000000000001
    }

    """
    logger.debug(f"Subtracting the number {a} from the number {b}")
    return operator.sub(a, b)
    

@jsonrpc.method('calc.mul')
def mul(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "3.0",
            "method": "calc.mul",
            "params": {"a": 6.8, "b": 9.3},
            "id": "1"
        }' http://localhost:5000/api
    
    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.1.3 Python/3.10.11
    Date: Tue, 21 Jan 2025 02:22:56 GMT
    Content-Type: application/json
    Content-Length: 55
    Connection: close

    {
      "id": "1",
      "jsonrpc": "3.0",
      "result": 63.24
    }
    """
    logger.debug(f"Multiplying the numbers {a} and {b}")
    return operator.mul(a, b)


@jsonrpc.method('calc.truediv')
def truediv(a: float, b: float) -> float:
    """
    Пример запроса:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
            "jsonrpc": "3.0",
            "method": "calc.truediv",
            "params": {"a": 46.8, "b": 7.0},
            "id": "1"
        }' http://localhost:5000/api
    
    Пример ответа:

    HTTP/1.1 200 OK
    Server: Werkzeug/3.1.3 Python/3.10.11
    Date: Tue, 21 Jan 2025 02:26:36 GMT
    Content-Type: application/json
    Content-Length: 67
    Connection: close

    {
      "id": "1",
      "jsonrpc": "3.0",
      "result": 6.685714285714285
    }

    Пример ответа при делении на 0:

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
        -d '{
                "jsonrpc": "3.0",
                "method": "calc.truediv",
                "params": {"a": 46.8, "b": 0.0},
                "id": "1"
            }' http://localhost:5000/api
    HTTP/1.1 200 OK
    Server: Werkzeug/3.1.3 Python/3.10.11
    Date: Tue, 21 Jan 2025 02:27:36 GMT
    Content-Type: application/json
    Content-Length: 53
    Connection: close

    {
      "id": "1",
      "jsonrpc": "3.0",
      "result": 0.0
    }
    """
    try:
        logger.debug(f"Dividing the number {a} by the number {b}")
        return operator.truediv(a, b)
    except ZeroDivisionError as err:
        logger.error("You can't divide by zero.")
        logger.exception(err)
        return 0.0


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
