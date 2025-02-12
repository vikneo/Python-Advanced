"""
В этом файле будет ваше Flask-приложение
"""
import csv
import re
from typing import Type
from datetime import datetime

from flask import render_template, request, redirect, flash, url_for

from models import Base, Profile, User
from forms import UploadFileCSV
from config import Session, engine, app, save_upload_file
from generic_data import create_csv


def check_field_name(file_name: str) -> (tuple[list[str], Type[User]] |
                                        tuple[list[str], Type[Profile]]):
    file = re.findall(r'[\w.\w\s]+', file_name)
    name = file[-1].split('.')[0]
    if name == 'users':
        return ['email', 'pswd'], User
    elif name == 'profiles':
        return ['name', 'surname', 'phone','subscribe', 'user_id'], Profile


@app.before_request
def before_request():
    Base.metadata.create_all(bind = engine)


@app.route('/', methods = ['GET'])
def index():
    create_file = request.args.get('create_file')
    search = request.args.get('search')
    if create_file:
        try:
            create_csv.run()  # TODO добавить в задачи Celery
            flash('Файлы `user.csv & profile.csv` успешно созданы', 'success')
        except Exception as err:
            flash(f'Сообщение: {err}', 'error')
    if search:
        flash(f'Результат поиска по: {request.args.get("search")}', 'success')
        users = Profile.get_user_by_name(search.capitalize())
        return render_template("base/search.html", users=users, title=f'Результат поиска по {search}'), 200
    return render_template("base/index.html", title='Celery'), 200


@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_csv_file():
    """
    Endpoint for download file type csv and save data in table
    """
    form = UploadFileCSV()
    if form.validate_on_submit():
        file_csv = save_upload_file(form.file.data)
        with open(file_csv, 'r') as file:
            fieldnames, _model = check_field_name(file_csv)
            read_file = csv.DictReader(f = file, fieldnames = fieldnames, delimiter = ';')
            data_table = []
            for std in read_file:
                if 'subscribe' in std:
                    std['subscribe'] = bool(std['subscribe'])
                data_table.append(std)
            with Session() as session:
                session.bulk_insert_mappings(_model, data_table)
                session.commit()
        flash(f"Загрузка файла `{form.file.data.filename}` прошла успешно", "success")
        return redirect(url_for('index'))

    return render_template('base/upload_file.html', form = form, title = 'Загрузка файла')


@app.route('/blur', methods=['GET', 'POST'])
def bluray_images():
    """
    Ставит в очередь обработку переданных изображений. 
    Возвращает ID группы задач по обработке изображений.
    """
    pass


@app.route('/status/<int:id>', methods=['GET'])
def get_status_task_id(id):
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач) 
    и статус (в процессе обработки, обработано).
    """
    pass


@app.route('/subscribe', methods=['GET', 'POST'])
def subscription_to_newsletter():
    """
    Пользователь указывает почту и подписывается на рассылку. 
    Каждую неделю ему будет приходить письмо о сервисе на почту
    """
    pass


@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscription_from_newsletter():
    """
    Пользователь указывает почту и отписывается от рассылки
    """
    pass


if __name__ == '__main__':
    app.run(debug = True)