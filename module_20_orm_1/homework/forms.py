from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, BooleanField
from wtforms.validators import InputRequired, Email


class BookAddForm(FlaskForm):
    """
    Форма для создания книги
    """
    name = StringField(u'Название: ', validators=[InputRequired()])
    count = IntegerField(u'Количество: ', validators=[InputRequired()])
    release_date = StringField(u'Дата релиза: ', validators=[InputRequired()])
    author_id = IntegerField(u'Автор ID: ', validators=[InputRequired()])


class AuthorAddForm(FlaskForm):
    """
    Форма для добавления Автора
    """
    name = StringField(u'Имя', validators=[InputRequired()])
    surname = StringField(u'Фамилия', validators=[InputRequired()])


class StudentAddFrom(FlaskForm):
    """
    Форма для добавления студентов
    """
    name = StringField(u'Имя', validators=[InputRequired()])
    surname = StringField(u'Фамилия', validators=[InputRequired()])
    phone = StringField(u'Телефон', validators=[InputRequired()])
    email = StringField(u'Email', validators=[Email("Не верный email")])
    average_score = FloatField(u'Средний балл', validators=[InputRequired()])
    scholarship = BooleanField(u'Стипендия', validators=[InputRequired()])


class ReceivingBooksAddForm(FlaskForm):
    """
    Форма для добавления читающих
    """
    book_id = IntegerField(u'ID Книги', validators=[InputRequired()])
    student_id = IntegerField(u'ID Студента', validators=[InputRequired()])
    date_of_return = StringField(u'Дата возврата',)
