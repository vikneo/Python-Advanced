"""
В этом файле будут Celery-задачи
"""
import re

from celery import Celery
from sqlalchemy import select

from config import app, Session
from image import blur_image
from mail import send_email
from models import User, Profile


celery = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery.task
def image_processing(image: str):
    """
    Обработка изображения с эфектом размытия
    """
    filename = re.findall(r'[\w.\w\s]+', image)[-1]
    blur_image(image)
    return f"Обработано изображение ```{filename}```"


@celery.task
def send_an_email(email: str = None, order_id: str =None, filename: str = None, _text: str = None):

    if email is None:
        with Session() as session:
            users = session.execute(
                select(User.email).filter(Profile.subscribe == True).where(Profile.user_id == User.id)
            ).all()
            for user in users:
                send_email(
                    order_id=order_id,
                    receiver=user,
                    filename=filename,
                    _text = _text
                )
    else:
        send_email(
            order_id=order_id,
            receiver=email,
            filename=filename,
            _text = _text
        )
