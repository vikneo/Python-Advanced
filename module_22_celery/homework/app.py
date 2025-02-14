"""
В этом файле будет ваше Flask-приложение
"""
import csv
import re
from typing import Type
from datetime import datetime

from celery import group
from flask import render_template, request, redirect, flash, url_for

from models import Base, Profile, User
from forms import UploadFileCSV, FileForm, SubscribeForm
from config import Session, engine, app, save_upload_file
from generic_data import create_csv
from celery_tasks import image_processing, send_an_email


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
            create_csv.run()  # TODO добавить в задачи Celery
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
        group_task = task_group.apply_async()

        flash(f'Добавлена группа задач с ID {group_task.id}', 'success')
        # return redirect(url_for('index'))
        return render_template('base/index.html', group_id=group_task.id)
    return render_template('images/upload_images.html', form = form, title = 'Обработка фотографий'), 200


@app.route('/status', methods = ['GET'])
def get_status_task_id():
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач) 
    и статус (в процессе обработки, обработано).

    ------------------------------------------------------
    Пробное решение отправки письма на почту пользователя
    -------------------------------------------------------
    РЕШЕНО
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    email = MIMEMultipart()

    passwd = 'passworf' # пароль сгенерированный от безопастности для сторонних приложений почтового сервиса
    email['Subject'] = 'Test email'
    email['From'] = 'email' # адрес почты
    email['To'] = 'addresat'

    email.attach(MIMEText("Thank you", 'plain'))
    # email.attach(MIMEImage(file("google.jpg").read()))

    server = smtplib.SMTP('smtp.mail.ru: 587')
    server.starttls()

    server.login(email['From'], passwd)
    server.sendmail(email['From'], email['To'], email.as_string())
    server.quit()
    flash('Вам отправлено письмо', 'success')
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
            
            Profile.subscribes(user_id=user.id, data=True)
            # send_an_email(
            #     email=user.email,
            #     order_id='Поздравляем вы подписаны на новые уведомления.',
            #     _text = f'Так как указали свой почтовый адрес <{user.email}>'
            # )
            flash('Вы успешно подписаны. Уведомление отправлено на почту', 'success')
            return redirect(url_for('index'))
        else:
            flash('Не найден пользователь с таким email', 'error')

    return render_template('users/subscribe.html', form=form, title='Оформление подписки')


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
                Profile.subscribes(user_id=user.id, data=False)
                flash(f'Адрес ``{user.email}`` отписан от рассылок. Изменить параметры можете в ', 'success')
                # Здесь отправка письма - уведомление
                return render_template('base/index.html', target=user.id)
            else:
                flash('У вас нет активных рассылок', 'warning')    
        else:
            flash('Не найден пользователь с таким email', 'error')

    return render_template('users/subscribe.html', form=form, title='Отказ от получения сообщений с сайта')


def start_docker():
    pass


def start_celety():
    pass

if __name__ == '__main__':
    app.run(debug = True)
