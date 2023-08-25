from rest_framework.exceptions import ValidationError


def validate_tags_amount(tags):
    if len(tags) > 5:
        raise ValidationError('Максимальное количество тегов - 5.')
    elif len(tags) < 1:
        raise ValidationError('Вы не можете создать вопрос без тегов.')


def validate_related_obj_amount():
    pass


def validate_question_related_obj_amount(uploaded_images):
    if len(uploaded_images) > 3:
        raise ValidationError('Максимально допустимое число вложений - 3.')


def validate_answer_related_obj_amount(uploaded_images):
    if len(uploaded_images) > 1:
        raise ValidationError('Максимально допустимое число вложений - 1.')

