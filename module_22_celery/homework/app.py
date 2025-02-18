"""
В этом файле будет ваше Flask-приложение
"""
import csv
import re
import shlex
import subprocess
import zipfile
from typing import Type

from celery import group, chain
from flask import render_template, request, redirect, flash, url_for, jsonify

from models import Base, Profile, User
from forms import UploadFileCSV, FileForm, SubscribeForm
from config import Session, engine, app, save_upload_file
from celery_tasks import image_processing, send_mail_to_subscribe, celery, create_csv_file


def check_field_name(file_name: str) -> (tuple[list[str], Type[User]] |
                                         tuple[list[str], Type[Profile]]):
    file = re.findall(r'[\w.\w\s]+', file_name)
    name = file[-1].split('.')[0]
    if name == 'users':
        return ['email', 'pswd'], User
    elif name == 'profiles':
        return ['name', 'surname', 'phone', 'subscribe', 'user_id'], Profile


@app.before_request
def before_request():
    Base.metadata.create_all(bind = engine)


@app.route('/', methods = ['GET'])
def index():
    create_file = request.args.get('create_file')
    search = request.args.get('search')

    if create_file:
        try:
            create_csv_file.delay()
            flash('Файлы `user.csv & profile.csv` успешно созданы', 'success')
        except Exception as err:
            flash(f'Сообщение: {err}', 'error')
    if search:
        flash(f'Результат поиска по: {request.args.get("search")}', 'success')
        users = Profile.get_user_by_name(search.capitalize())
        return render_template("base/search.html", users = users, title = f'Результат поиска по {search}'), 200
    return render_template("base/index.html", title = 'Celery'), 200


@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_csv_file():
    """
    Endpoint for download file type csv and save data in table
    """
    form = UploadFileCSV()
    if form.validate_on_submit():
        for _file in form.file.data:
            file_csv = save_upload_file(_file)
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
            flash(f"Загрузка файла `{_file.filename}` прошла успешно", "success")
        return redirect(url_for('index'))

    return render_template('base/upload_file.html', form = form, title = 'Загрузка файла')


# -----------------------------------------------------------------------
# MODULE 22 tasks
# -----------------------------------------------------------------------

def get_aip_archive(result: celery.GroupResult) -> str:
    file_zip = 'images_blur.zip'
    with zipfile.ZipFile(file_zip, 'w') as _object:
        for file in result:
            _object.write(file.get(), compress_type = zipfile.ZIP_DEFLATED)
    return file_zip


@app.route('/blur', methods = ['GET', 'POST'])
def blurry_images():
    """
    Ставит в очередь обработку переданных изображений. 
    Возвращает ID группы задач по обработке изображений.
    """
    form = FileForm()
    if form.validate_on_submit():
        new_list_img = [save_upload_file(image) for image in form.file.data]

        task_group = group(image_processing.s(_image) for _image in new_list_img)
        res = chain(task_group)
        chain_tasks = res.delay()
        send_mail_to_subscribe.delay(
            title = 'Обработка изображений',
            email = 'vm-viktor@mail.ru',  # тестовый почтовый ящик
            filename = get_aip_archive(chain_tasks),
            message = f'Изображения обработаны.\nВаш идентификатор {chain_tasks.id}\nСкачать можете по ссылке <здесь>'
        )

        group_task = task_group.apply_async()
        group_task.save()

        flash(f'Ващ заказ с № `{group_task.id}`. Статус заказа можете отследить ',
              'success')
        return render_template('base/index.html', group_id = group_task.id, task_id = group_task.id)

    return render_template('images/upload_images.html', form = form, title = 'Обработка фотографий'), 200


@app.route('/status/<group_id>', methods = ['GET'])
def get_status_task_id(group_id: str):
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач) 
    и статус (в процессе обработки, обработано).
    """
    result = celery.GroupResult.restore(group_id)
    if result:
        status_tasks = result.completed_count() / len(result)

        if int(status_tasks) != 1:
            flash("Изображения еще обрабатываются", 'success')
            return redirect(url_for('index'))

        status = {
            "group_id": group_id,
            "code": jsonify({"status": status_tasks}),
            "count_tasks": len(result),
            "completed": status_tasks * 100
        }

        flash("Вам отправлен архив с фотографиями. Проверьте почту", 'success')
        return render_template('users/task_id.html',
                               status = status,
                               title = 'Статус группы задач')
    flash('Отсутствуют активные задачи', 'success')
    return redirect(url_for('index'))


@app.route('/subscribe', methods = ['GET', 'POST'])
def subscription_to_newsletter():
    """
    Пользователь указывает почту и подписывается на рассылку. 
    Каждую неделю ему будет приходить письмо о сервисе на почту
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.get_user_by_email(email)

        if user:
            if user.profile.subscribe:
                flash('Вы уже подписаны', 'warning')
                return redirect(url_for('index'))

            Profile.subscribes(user_id = user.id, data = True)
            send_mail_to_subscribe.delay(
                email = 'vm-viktor@mail.ru',
                order_id = 'Поздравляем вы подписаны на новые уведомления.',
                _text = f'Так как указали свой почтовый адрес <{user.email}>'
            )
            flash('Вы успешно подписаны. Уведомление отправлено на почту', 'success')
            return redirect(url_for('index'))
        else:
            flash('Не найден пользователь с таким email', 'error')

    return render_template('users/subscribe.html', form = form, title = 'Оформление подписки')


@app.route('/unsubscribe', methods = ['GET', 'POST'])
def unsubscription_from_newsletter():
    """
    Пользователь указывает почту и отписывается от рассылки
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.get_user_by_email(email)

        if user:
            if user.profile.subscribe:
                Profile.subscribes(user_id = user.id, data = False)
                flash(f'Адрес ``{user.email}`` отписан от рассылок. Изменить параметры можете в ', 'success')
                # Здесь отправка письма - уведомление
                return render_template('base/index.html', target = user.id)
            else:
                flash('У вас нет активных рассылок', 'warning')
        else:
            flash('Не найден пользователь с таким email', 'error')

    return render_template('users/subscribe.html', form = form, title = 'Отказ от получения сообщений с сайта')


def start_docker():
    command_ctr = 'docker start my-redis'
    command = shlex.split(command_ctr)
    print('Запускаем докер')
    subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)


def start_celery():
    command_ctr = 'celery -A celery_tasks:celery worker -B'
    # command_ctr = 'celery -A celery_tasks:celery flower'
    command = shlex.split(command_ctr)
    print('Запускаем Celery')
    subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)


if __name__ == '__main__':
    app.run(debug = True)
