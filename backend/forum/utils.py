from __future__ import annotations

import json

from django.conf import settings
from django.core.cache import cache

from accounts.models import NewUser

from . import models


def invalidate_questions_solved(user: NewUser) -> None:
    """
    Удаляет кэш количества решенных вопросов пользователя.
    """
    data = json.dumps({'user_id': user.pk, 'key': settings.QUESTION_SOLVED_NAME})
    cache.delete(data)
