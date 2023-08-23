from typing import Iterator

from accounts.models import NewUser
from django.db.models import Count, QuerySet
from rest_framework.exceptions import ValidationError

from forum.models import Question, ThemeTag


def create_return_tags(tags: list, user: NewUser) -> Iterator[int]:
    """
    Yields tags. If tag does not exist, create it marking the tag as
    user's non-relevant tag. Returns tag ID.
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
