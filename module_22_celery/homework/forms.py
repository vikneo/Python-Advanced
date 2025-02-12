from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class UploadFileCSV(FlaskForm):
    """
    Форма для загрузки файла csv
    """
    file = FileField(u'Файл .csv', validators = [FileRequired()])
    