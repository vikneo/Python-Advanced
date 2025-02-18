"""
В этом файле будут Celery-задачи
"""
import re

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select

from config import app, Session
from image import blur_image
from mail import send_email
from models import User, Profile
from generic_data import create_csv

celery = Celery(
    app.name,
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0',
    broker_connection_retry_on_startup = True
)


@celery.task
def create_csv_file():
    create_csv.run()
    return "Create file csv"


@celery.task
def image_processing(image: str):
    """
    Обработка изображения с эфектом размытия
    """
    blur_img = blur_image(image)
    return blur_img


@celery.on_after_finalize.connect
def periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour = '13', minute = '38', day_of_week = 'Friday'),
        send_an_email.s(
            title = 'Обновленная линейка',
            message = 'Если вы получили письмо ошибочно, проигнорируйте его. Вы в праве отказаться от рассылок'
        ),
        name = 'periodic task'
    )
    return "Отправлено"


@celery.task
def send_an_email(title: str, filename: str = None, message: str = None):
    with Session() as session:
        users = session.execute(
            select(User.email).filter(Profile.subscribe == True).where(Profile.user_id == User.id)
        ).all()
        print(users)
        for email in users:
            send_email(
                order_id = title,
                receiver = email[0],
                filename = filename,
                _text = message
            )
    return "Письма разосланы"


@celery.task(bing = True)
def send_mail_to_subscribe(email: str, title: str, filename: str = None, message: str = None):
    send_email(
        order_id = title,
        receiver = email,
        filename = filename,
        _text = message
    )
    return "Письмо отправлено"
