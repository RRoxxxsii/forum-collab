from __future__ import annotations

import re

from django.contrib.auth.models import AnonymousUser

from accounts.models import NewUser
from forum.models import Question, QuestionAnswer, AnswerComment
from forum.repository import QuestionRepository, ThemeTagRepository, AnswerRepository, CommentRepository
from notifications.utils import notify


class QuestionService:
    question_repository = QuestionRepository
    tag_repository = ThemeTagRepository

    @classmethod
    def create_question(cls, user: NewUser, title: str, content: str, tags: list, images: list = None) -> Question:
        question = cls.question_repository.create_question(title=title, content=content, user=user)
        tags = cls.tag_repository.create_tags(tags=tags, user=user)

        if images:
            cls.question_repository.add_attachments(parent=question, attachments=images)

        cls.question_repository.add_tags(question=question, tags=tags)
        return question


class AnswerService:
    answer_repository = AnswerRepository

    @classmethod
    def create_answer(
            cls, question: Question, answer: str, images: list = None, user: NewUser = None
                      ) -> QuestionAnswer:

        answer = cls.answer_repository.create_answer(question=question, answer=answer, user=user)
        if images:
            cls.answer_repository.add_attachments(parent=answer, attachments=images)

        notify(
            sender=user, receiver=question.user,
            text='ответил на ваш вопрос', action_obj=answer,
            target=question
        )

        return answer


class CommentService:
    comment_repository = CommentRepository
    answer_repository = AnswerRepository

    @classmethod
    def parse_comment(cls, comment: str) -> [NewUser | None]:
        """
        Проверка, есть ли упоминание других пользователей в комментарии.
        """
        pattern = r'@[a-zA-Z0-9_]+'
        result = re.findall(pattern, comment)
        for match in result:
            # if NewUser.objects.filter(user_name=match).exists():
            match = match.strip('@')
            try:
                user = NewUser.objects.get(user_name=match)
            except NewUser.DoesNotExist:
                pass
            else:
                yield user

    @classmethod
    def create_comment(
            cls, comment: str, question_answer_id: int, parent_id: int, user: NewUser | AnonymousUser
                       ) -> AnswerComment:

        if isinstance(user, AnonymousUser):
            user = None

        answer = cls.answer_repository.get_answer_by_id(question_answer_id)
        answer_user = answer.user

        comment = cls.comment_repository.create_comment(
            comment=comment, question_answer=answer, parent_id=parent_id, user=user
        )

        if parent_id:
            parent = cls.comment_repository.get_comment_by_id(parent_id)
            parsed_user_iterable = cls.parse_comment(comment=comment.comment)

            for parsed_user in parsed_user_iterable:
                notify(
                    sender=user, receiver=parsed_user,
                    text='ответил на ваш комментарий',
                    action_obj=comment,
                    target=parent
                )

        if answer_user:
            notify(
                sender=user, receiver=answer_user,
                text='прокомментировал ваш ответ на вопрос',
                target=answer, action_obj=comment
            )

        return comment
