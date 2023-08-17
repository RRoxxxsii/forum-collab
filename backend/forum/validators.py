from django.core.exceptions import ValidationError


def validate_tags(value):
    if len(value) > 5:
        raise ValidationError('Максимальное количество тегов - 5')
