from __future__ import annotations

import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from accounts.cache_manager import CacheManager
from accounts.models import NewUser
from forum.models import AnswerComment, Question, QuestionAnswer
from forum.repository import (AnswerRepository, CommentRepository,
                              LikeDislikeRepository, QuestionRepository,
                              ThemeTagRepository)
from notifications.utils import notify


class LikeDislikeService:
    repository = LikeDislikeRepository

    @classmethod
    def like(cls, user: NewUser, obj: Question | QuestionAnswer):
        # если у пользователя не стоит лайк
        if user not in cls.repository.get_users_liked(obj):
            # если у пользователя не стоит дизлайк
            if user not in cls.repository.get_users_disliked(obj):
                # ставим лайк
                cls.repository.set_like(obj, user)
            # если у пользователя стоит дизлайк
            else:
                cls.repository.remove_dislike(obj, user)
                cls.repository.set_like(obj, user)
        # если у пользователя уже стоит лайк
        else:
            cls.repository.remove_like(obj, user)

        obj.rating.save()

    @classmethod
    def dislike(cls, user: NewUser, obj: Question | QuestionAnswer):
        # если у пользователя не стоит дизлайк
        if user not in cls.repository.get_users_disliked(obj):
            # если у пользователя не стоит лайк
            if user not in cls.repository.get_users_liked(obj):
                # ставим дизлайк
                cls.repository.set_dislike(obj, user)
            # если у пользователя стоит лайк
            else:
                # убираем лайк
                cls.repository.remove_like(obj, user)
                # ставим дизлайк
                cls.repository.set_dislike(obj, user)
        # если у пользователя уже стоит дизлайк
        else:
            # убираем дизлайк
            cls.repository.remove_dislike(obj, user)

        obj.rating.save()


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

    @classmethod
    def make_tag_relevant_on_question_save(cls, question: Question) -> None:
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

    @staticmethod
    def vote_answer_solving(answer: QuestionAnswer, related_question: Question, user: NewUser):
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

        CacheManager.delete_cache_data(user_id=user.pk, key_prefix=settings.QUESTION_SOLVED_NAME)


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

        answer = cls.answer_repository.get_obj_by_id(question_answer_id)
        answer_user = answer.user

        comment = cls.comment_repository.create_comment(
            comment=comment, question_answer=answer, parent_id=parent_id, user=user
        )

        if parent_id:
            parent = cls.comment_repository.get_obj_by_id(parent_id)
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
