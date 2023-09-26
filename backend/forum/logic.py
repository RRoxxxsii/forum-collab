from __future__ import annotations

import re
from typing import Iterator

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from accounts.models import NewUser
from forum.models import (Question, QuestionAnswer, QuestionAnswerImages,
                          QuestionImages, ThemeTag)
from notifications.utils import notify


def create_return_tags(tags: list, user: NewUser) -> Iterator[int]:
    """

    Возвращает ID тегов с помощью yield. Если тега не существует, если тега не существует,
    создает тег как пользовательский нерелвантный.
    """
    for tag in tags:

        tag, created = ThemeTag.objects.get_or_create(tag_name=tag, defaults={
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

    suggested_tags = ThemeTag.objects.filter(tag_name__icontains=tag).order_by('is_user_tag')

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


def vote_answer_solving(answer: QuestionAnswer, related_question: Question):
    """
    Отмечает ответ как решивший проблему. Если данный вопрос отмечен и на него поступает
    запрос, отметка вопроса как решившего проблему снимается, как и отметка вопроса как решенного.
    Если ответ не отмечен как решающий и для вопроса нет решающих ответов, тогда ответ
    отмечается как решающим, а вопрос как решенным, если же есть другой решающий ответ,
    метка решающего ответа с него снимается и ставится на другой ответ.
    """
    if answer.is_solving:
        answer.is_solving = False
        related_question.is_solved = False
    else:
        if related_question.question_answers.filter(is_solving=True).exists():
            is_solving_answer = related_question.question_answers.get(is_solving=True)
            is_solving_answer.is_solving = False
            is_solving_answer.save()
        answer.is_solving = True
        related_question.is_solved = True

        notify(target=answer, receiver=answer.user, text='ваш ответ отмечен как решающий',
               sender=related_question.user)

    related_question.save()
    answer.save()


def parse_comment(comment: str) -> [NewUser | None]:
    """
    Проверка, есть ли упоминание других пользователей в комментарии.
    """
    pattern = r'(\s|^)?@[a-zA-Z0-9_]+,?.+(\s|$)'
    result = re.findall(r'@[a-zA-Z0-9_]+', comment)
    for match in result:
        # if NewUser.objects.filter(user_name=match).exists():
        match = match.strip('@')
        try:
            user = NewUser.objects.get(user_name=match)
        except NewUser.DoesNotExist:
            pass
        else:
            yield user
