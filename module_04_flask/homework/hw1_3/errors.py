"""
Модуль кастомных ошибок
"""

from wtforms.validators import ValidationError


class InvalidIntegerError(ValidationError):
    """
    Индивидуальный класс, для генерации ошибки
    при проверке полей связанных только с типом "число"
    """
    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class InvalidNameError(ValidationError):
    """
    Индивидуальный класс, для генерации ошибки при
    проверке вводимого ФИО с шаблоном.
    Шаблон: Фамилия И.О.
    """
    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
