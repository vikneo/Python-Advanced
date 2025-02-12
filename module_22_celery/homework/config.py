"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""
import os

from flask import Flask, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename


# --------------------------------------------------------------------------------------
# Session service & paths for data
# --------------------------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
PATH_TO_DB = os.path.join(BASE_DIR, 'mod_22_celery.db')
DIR_FILE = 'files'
os.makedirs(os.path.join(BASE_DIR, DIR_FILE), exist_ok = True)

PATH_TO_FILE = os.path.join(BASE_DIR, DIR_FILE)

ALLOWED_EXTENSIONS = ['csv']

engine = create_engine(f'sqlite:///{PATH_TO_DB}')
Session = sessionmaker(engine)

app = Flask(__name__)
app.secret_key = 'asdasdasdsaw2qeqasdfw43r5'
app.config['UPLOAD_FOLDER'] = PATH_TO_FILE


# --------------------------------------------------------------------------------------
# POST service
# --------------------------------------------------------------------------------------
# https://yandex.ru/support/mail/mail-clients/others.html

SMTP_USER = "ПОЧТА ОТПРАВИТЕЛЯ"
SMTP_HOST = "smtp.yandex.com"
SMTP_PASSWORD = "ПАРОЛЬ ОТ ПОЧТЫ ОТПРАВИТЕЛЯ / СПЕЦИАЛЬНЫЙ ТОКЕН ПРИЛОЖЕНИЯ"
SMTP_PORT = 587


# --------------------------------------------------------------------------------------
# checking the file extension
# --------------------------------------------------------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(file: str) -> str:
    if file.filename == '':
        flash('No selected file', 'error')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_to_file)
        return path_to_file

