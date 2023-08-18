from rest_framework.exceptions import ValidationError

from forum.models import ThemeTag


def validate_tags_amount(tags):
    if len(tags) > 5:
        raise ValidationError('Максимальное количество тегов - 5.')
    elif len(tags) < 1:
        raise ValidationError('Вы не можете создать вопрос без тегов.')
