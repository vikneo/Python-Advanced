from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms.validators import InputRequired
from wtforms.fields.simple import StringField


class UploadFileCSV(FlaskForm):
    """
    Форма для загрузки файла csv
    """
    file = MultipleFileField(u'Файл .csv', validators = [FileRequired()])


class FileForm(FlaskForm):
    """
    Форма для загрузки изображений
    """
    file = MultipleFileField(u'Выберите изображения', validators = [FileRequired()])


class SubscribeForm(FlaskForm):
    """
    Форма для оформления подписки и возможность отписаться от рассылки
    """
    email = StringField(u'Введите вашу почту', validators=[InputRequired()])
