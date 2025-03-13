from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import Field

from typing import Optional


class TimeLimit:
    """
    Validator for the field "timeout"
    """
    def __init__(self, limit_max: int = 30, message: Optional[str] = None):
        """
        default limit_max is 30 sec
        """
        self.limit_min = 0
        self.limit_max = limit_max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field, message: Optional[str] = None) -> None:

        if not isinstance(field.data, int):
            self.message = "Field must be an integer"
            raise ValidationError(self.message)

        if field.data < self.limit_min:
            self.message = "The time must be a positive number"
            raise ValidationError(self.message)
        elif field.data > self.limit_max:
            self.message = f"The time must not exceed {self.limit_max}"
            raise ValidationError(self.message)