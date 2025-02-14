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

os.makedirs(os.path.join(PATH_TO_FILE, 'csv_file'), exist_ok = True)
os.makedirs(os.path.join(PATH_TO_FILE, 'image_file'), exist_ok = True)
PATH_TO_FILE_CSV = os.path.join(PATH_TO_FILE, 'csv_file')
PATH_TO_FILE_IMAGES = os.path.join(PATH_TO_FILE, 'image_file')

ALLOWED_EXTENSIONS_CSV = ['csv']
ALLOWED_EXTENSIONS_IMG = ['jpg', 'jpeg', 'png', 'gif']

engine = create_engine(f'sqlite:///{PATH_TO_DB}')
Session = sessionmaker(engine)

app = Flask(__name__)
app.secret_key = 'asdasdasdsaw2qeqasdfw43r5'
app.config['UPLOAD_FOLDER_CSV'] = PATH_TO_FILE_CSV
app.config['UPLOAD_FOLDER_IMAGES'] = PATH_TO_FILE_IMAGES


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

def allowed_file_csv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_CSV


def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG


def save_upload_file(file: str) -> str | bytes:
    if file.filename == '':
        flash('No selected file', 'error')

    if file.filename.split('.')[-1] == 'csv':
        if file and allowed_file_csv(file.filename):

            filename = secure_filename(file.filename)
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER_CSV'], filename)
            file.save(path_to_file)
            return path_to_file
    else:
        if file and allowed_file_img(file.filename):
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], file.filename)
            file.save(path_to_file)
            return path_to_file
