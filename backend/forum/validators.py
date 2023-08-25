from functools import wraps

from rest_framework.exceptions import ValidationError


def validate_tags_amount(tags):
    """
    Валидация тегов. Запрещается создавать вопрос без тегов, и с более 5 тегами.
    """
    if len(tags) > 5:
        raise ValidationError('Максимальное количество тегов - 5.')
    elif len(tags) < 1:
        raise ValidationError('Вы не можете создать вопрос без тегов.')


def max_attachments_validator(max_attachments):
    def decorator(func):
        @wraps(func)
        def wrapper(uploaded_images):
            if len(uploaded_images) > max_attachments:
                raise ValidationError(f'Максимально допустимое число вложений - {max_attachments}.')
            return func(uploaded_images)
        return wrapper
    return decorator


@max_attachments_validator(max_attachments=3)
def validate_question_related_obj_amount(uploaded_images):
    """
    Валидация числа вложений вопроса.
    """
    pass


@max_attachments_validator(max_attachments=1)
def validate_answer_related_obj_amount(uploaded_images):
    """
    Валидация числа вложений вопроса.
    """
    pass
