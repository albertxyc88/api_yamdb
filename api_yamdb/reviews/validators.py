import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    if year > datetime.datetime.now().year:
        raise ValidationError(
            (f'Введенный {year} год не может быть больше текущего!')
        )
