from __future__ import annotations

from typing import Iterator

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from accounts.models import NewUser
from forum.models import (Question, QuestionAnswer, QuestionAnswerImages,
                          QuestionImages, ThemeTag)


def create_return_tags(tags: list, user: NewUser) -> Iterator[int]:
    """

    Возвращает ID тегов с помощью yield. Если тега не существует, если тега не существует,
    создает тег как пользовательский нерелвантный.
    """
    for tag in tags:

        tag, created = ThemeTag.objects.get_or_create(tag=tag, defaults={
            'is_user_tag': True,
            'is_relevant': False,
            'user': user
        })

        yield tag.id


def get_tags_or_error(tag: str) -> QuerySet[ThemeTag]:
    """
    Возрвщает список тегов или возбуждает исключение.
    """
    if not tag:
        raise ValidationError('Тег не указан.')

    suggested_tags = ThemeTag.objects.filter(tag__icontains=tag).order_by('is_user_tag')

    if not suggested_tags:
        raise ValidationError('Теги не указан.')

    return suggested_tags


def make_tag_relevant_on_question_save(question: Question):
    """
    Делает релеватными тег, количество вопросов по которому >= 10.
    """
    tags = question.tags.filter(is_user_tag=True, is_relevant=False)
    for tag in tags:
        if tag.questions.count() >= 10:
            tag.is_relevant = True
            tag.save(update_fields=['is_relevant'])


def add_image(images: list, obj_model: [Question | QuestionAnswer],
              attachment_model: [QuestionImages | QuestionAnswerImages]):
    """
    Создание вложений(фотографий) для поста.
    """
    for image in images:
        attachment_model.objects.create(image=image, parent=obj_model)
