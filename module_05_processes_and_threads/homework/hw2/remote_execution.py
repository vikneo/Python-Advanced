"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import shlex
import subprocess

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, ValidationError

from validators import TimeLimit

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), TimeLimit()])


def run_python_code_in_subprocess(code: str, timeout: int):
    """
    simple example sting code:
    print(2**2**10); shell=True -> err
    print(2**2**100) if timeout=1-> err
    print(2**2**10) -> out
    print('Hacked') -> out
    """
    cmd = f'prlimit --nproc=1:1 python -c "{code}"'

    if 'shell=True' in cmd:
        raise ValidationError('The shell=True expression cannot be used')

    cmd_list = shlex.split(cmd)
    process = subprocess.Popen(
        cmd_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        out, err = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return f"Код не уложился в данное время - {timeout}s"

    return out, err


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        try:
            result = run_python_code_in_subprocess(code, timeout)

            if isinstance(result, tuple):
                if result[0]:
                    return f"Результат выполнения кода: {result[0]}", 200
                return f"Завершилось с ошибкой {result[1]}", 400
            elif isinstance(result, str):
                return result, 400
        except Exception as err:
            return f"{err}", 400

    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
