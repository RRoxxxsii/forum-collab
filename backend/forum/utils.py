from __future__ import annotations

import json

from django.conf import settings
from django.core.cache import cache

from accounts.models import NewUser

from . import models


def invalidate_likes_cache(user: NewUser, instance: [models.Question | models.QuestionAnswer]) -> None:
    """
    Удаляет кэш лайков экземпляра класса ответов или вопросов.
    """
    if isinstance(instance, models.Question):
        data = json.dumps({'user_id': user.pk, 'key': settings.QUESTION_LIKE_NAME})
        cache.delete(data)
    elif isinstance(instance, models.QuestionAnswer):
        data = json.dumps({'user_id': user.pk, 'key': settings.ANSWER_LIKE_NAME})
        cache.delete(data)


def invalidate_dislikes_cache(user: NewUser, instance: [models.Question | models.QuestionAnswer]) -> None:
    """
    Удаляет кэш дизлайков экземпляра класса ответов или вопросов.
    """
    if isinstance(instance, models.Question):
        data = json.dumps({'user_id': user.pk, 'key': settings.QUESTION_DISLIKE_NAME})
        cache.delete(data)
    elif isinstance(instance, models.QuestionAnswer):
        data = json.dumps({'user_id': user.pk, 'key': settings.ANSWER_DISLIKE_NAME})
        cache.delete(data)


def invalidate_questions_solved(user: NewUser) -> None:
    """
    Удаляет кэш количества решенных вопросов пользователя.
    """
    data = json.dumps({'user_id': user.pk, 'key': settings.QUESTION_SOLVED_NAME})
    cache.delete(data)
