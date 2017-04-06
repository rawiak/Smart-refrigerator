from django.core.exceptions import ValidationError


def valid_range(value):
    if not 1 <= value <= 100:
        raise ValidationError('Zbyt mała liczba')
