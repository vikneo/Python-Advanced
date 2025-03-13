import time

from app import Fresh


application = Fresh()


@application.route('/', methods = ['GET'])
def index():
    return "Hello World!"


@application.route('/hello', methods = ['GET'])
def hello():
    return "Hello amigo!"


@application.route('/hello/<str:name>', methods = ['GET'])
def hello_with_name(name):
    return f'Hello {name} amigo!'


# @application.route('/long_task', methods = ['GET'])
# def long_task():
#     time.sleep(80)
#     return 'We did it!'
