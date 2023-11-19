from __future__ import annotations

import re
from typing import Iterator

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from accounts.models import NewUser
from forum.models import (Question, QuestionAnswer, QuestionAnswerImages,
                          QuestionImages, ThemeTag)
from notifications.utils import notify


def make_tag_relevant_on_question_save(question: Question):
    """
    Делает релеватными тег, количество вопросов по которому >= 10.
    Уведомляет пользователя, что тег релевантен.
    """
    tags = question.tags.filter(is_user_tag=True, is_relevant=False)
    for tag in tags:
        if tag.questions.count() >= 10:
            tag.is_relevant = True
            tag.save(update_fields=['is_relevant'])
            notify(receiver=tag.user, target=tag, text='тег становится релевантным')
