"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
import re
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from .errors import InvalidIntegerError, InvalidNameError


def number_length(min_value: int, max_value: int, message: Optional[str] = None):
    if message is None:
        message = "Номер телефона должен содержать только цифры"

    def _number_length(form: FlaskForm, field: Field) -> None:
        if field.data is None:
            raise InvalidIntegerError(message)

        if min_value > len(str(field.data)) < max_value and field.name == 'phone':
            _message = field.gettext("Номер телефона должен иметь длину 10 цифр и не начинаться с 0")
            raise InvalidIntegerError(_message)

        if min_value > len(str(field.data)) < max_value and field.name == 'index':
            _message = field.gettext("Должен иметь длину 6 цифр и не начинаться с 0")
            raise InvalidIntegerError(_message)

    return _number_length


class NumberLength:

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def __call__(self, form: FlaskForm, field: Field, message: Optional[str] = None) -> None:
        """
        Проверка на валидность вводимого числа как для поля с номером телефона, так и для поля с индексом
        :param form: форма
        :param field: поле с вводимым числом
        """
        if re.findall(r'[^ 0-9]', str(field.data)):
            raise InvalidIntegerError(f"В поле '{field.name}': 'Не допустимые символы'")

        if len(str(field.data)) != 6 and field.name.lower() == "index":
            self.message = field.gettext(f"Поле '{field.name}': 'Должно иметь длину 6 цифр и не начинаться с 0'")
            raise InvalidIntegerError(self.message)

        if len(str(field.data)) != 10 and field.name.lower() == "phone":
            self.message = field.gettext(f"Поле '{field.name}': 'Должно иметь длину 10 цифр и не начинаться с 0'")
            raise InvalidIntegerError(self.message)


class Name:
    def __call__(self, form: FlaskForm, field: Field, message: Optional[str] = None) -> None:
        """
        Проверка на валидность вводимого ФИО
        :param form: форма
        :param field: поле с фамилией и инициалами в формате Фамилия И.О.
        """
        if not re.findall(r"\b[A-ZА-Я][a-zа-я]* \b[A-ZА-Я].[A-ZА-Я].", field.data):
            raise InvalidNameError("{'name': 'ФИО должно содержать буквы и формат <<Фамилия И.О.>>'}")
