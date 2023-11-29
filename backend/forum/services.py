from __future__ import annotations

import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from accounts.cache_manager import CacheManager
from accounts.models import NewUser
from forum import repository
from forum.di import container
from forum.models import AnswerComment, Question, QuestionAnswer
from forum.querysets import CommentQSBase, QuestionAnswerQSBase, QuestionQSBase
from notifications.utils import notify


class LikeDislikeService:

    def __init__(self):
        self.repo: repository.AbstractLikeDislikeRepository = (
            container.resolve(repository.AbstractLikeDislikeRepository))

    def like(self, user: NewUser, obj: Question | QuestionAnswer):
        # если у пользователя не стоит лайк
        if user not in self.repo.get_users_liked(obj):
            # если у пользователя не стоит дизлайк
            if user not in self.repo.get_users_disliked(obj):
                # ставим лайк
                self.repo.set_like(obj, user)
            # если у пользователя стоит дизлайк
            else:
                self.repo.remove_dislike(obj, user)
                self.repo.set_like(obj, user)
        # если у пользователя уже стоит лайк
        else:
            self.repo.remove_like(obj, user)

    def dislike(self, user: NewUser, obj: Question | QuestionAnswer):
        # если у пользователя не стоит дизлайк
        if user not in self.repo.get_users_disliked(obj):
            # если у пользователя не стоит лайк
            if user not in self.repo.get_users_liked(obj):
                # ставим дизлайк
                self.repo.set_dislike(obj, user)
            # если у пользователя стоит лайк
            else:
                # убираем лайк
                self.repo.remove_like(obj, user)
                # ставим дизлайк
                self.repo.set_dislike(obj, user)
        # если у пользователя уже стоит дизлайк
        else:
            # убираем дизлайк
            self.repo.remove_dislike(obj, user)


class CreateQuestionService:

    def __init__(self):
        self.question_repo: repository.AbstractQuestionRepository = (
            container.resolve(repository.AbstractQuestionRepository))
        self.tag_repo: repository.AbsractThemeTagRepository = (
            container.resolve(repository.AbsractThemeTagRepository))

    def _create_question(self, user: NewUser, title: str, content: str, tags: list, images: list = None) -> Question:

        question = self.question_repo.create_question(title=title, content=content, user=user)
        tags = self.tag_repo.create_tags(tags=tags, user=user)

        if images:
            self.question_repo.add_attachments(parent=question, attachments=images)

        self.question_repo.add_tags(question=question, tags=tags)
        return question

    def execute(self, user: NewUser, title: str, content: str, tags: list, images: list = None):
        return self._create_question(user=user, title=title, content=content, tags=tags, images=images)


class MakeTagRelevantOnQuestionSave:

    def __init__(self):
        self.repo: repository.AbsractThemeTagRepository = (
            container.resolve(repository.AbsractThemeTagRepository))

    def _notify(self, receiver, target, text):
        return notify(receiver=receiver, target=target, text=text)

    def execute(self, question: Question) -> None:
        tags = question.tags.filter(is_user_tag=True, is_relevant=False)
        for tag in tags:
            if tag.questions.count() >= 10:
                self.repo.make_tag_relevant(tag)
                self._notify(receiver=tag.user, target=tag, text='тег становится релевантным')


class CreateAnswerService:

    def __init__(self):
        self.repo: repository.AbstractAnswerRepository = container.resolve(repository.AbstractAnswerRepository)

    def _create_answer(
            self, question: Question, answer: str, images: list = None, user: NewUser = None
                      ) -> QuestionAnswer:

        answer = self.repo.create_answer(question=question, answer=answer, user=user)
        if images:
            self.repo.add_attachments(parent=answer, attachments=images)

        return answer

    def _notify(
            self, sender: NewUser, receiver: NewUser,
            text: str, action_obj: QuestionAnswer,
            target: Question
                ) -> None:
        notify(
            sender=sender, receiver=receiver,
            text='ответил на ваш вопрос', action_obj=action_obj,
            target=target
            )

    def execute(
            self, question: Question, answer: str, images: list = None, user: NewUser = None
                ) -> QuestionAnswer:
        answer = self._create_answer(question, answer, images, user)
        self._notify(
            sender=user, receiver=question.user,
            text='ответил на ваш вопрос', action_obj=answer,
            target=question
                     )
        return answer


class VoteAnswerSolving:

    def __init__(self):
        self.repo: repository.AbstractAnswerRepository = container.resolve(repository.AbstractAnswerRepository)

    def _notify(self, target: QuestionAnswer, receiver: NewUser, text: str, sender: NewUser) -> None:
        notify(receiver=receiver, target=target, text=text, sender=sender)

    def execute(self, answer: QuestionAnswer, related_question: Question, user: NewUser):
        """
        Отмечает ответ как решивший проблему. Если данный вопрос отмечен и на него поступает
        запрос, отметка вопроса как решившего проблему снимается, как и отметка вопроса как решенного.
        Если ответ не отмечен как решающий и для вопроса нет решающих ответов, тогда ответ
        отмечается как решающим, а вопрос как решенным, если же есть другой решающий ответ,
        метка решающего ответа с него снимается и ставится на другой ответ.
        """
        queryset = QuestionQSBase()
        if answer.is_solving:
            self.repo.remove_is_solving_mark(answer=answer, question=related_question)
        else:
            if queryset.filter_solving_answers(related_question):
                is_solving_answer = queryset.get_solving_answer(related_question)
                self.repo.make_solving_answer_not_solving(is_solving_answer)

            self.repo.mark_answer_as_solving(answer=answer, question=related_question)

            self._notify(
                target=answer, receiver=answer.user, text='ваш ответ отмечен как решающий',
                sender=related_question.user
            )

        CacheManager.delete_cache_data(user_id=user.pk, key_prefix=settings.QUESTION_SOLVED_NAME)


class CreateComment:

    def __init__(self):
        self.answer_repo: repository.AbstractAnswerRepository = (
            container.resolve(repository.AbstractAnswerRepository))
        self.comment_repo: repository.AbstractCommentRepository = (
            container.resolve(repository.AbstractCommentRepository))

    def parse_comment(self, comment: str) -> [NewUser | None]:
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

    def _create_comment(
            self, comment: str, answer: QuestionAnswer, parent_id: int, user: NewUser
    ) -> AnswerComment:

        if isinstance(user, AnonymousUser):
            user = None

        comment = self.comment_repo.create_comment(
            comment=comment, question_answer=answer, parent_id=parent_id, user=user
        )

        return comment

    def _notify_parsed_users(self, parent_id: int, comment: AnswerComment, user: NewUser) -> None:
        if parent_id:
            parent = CommentQSBase().get_obj_by_id(parent_id)
            parsed_user_iterable = self.parse_comment(comment=comment.comment)
            for parsed_user in parsed_user_iterable:
                notify(
                    sender=user, receiver=parsed_user,
                    text='ответил на ваш комментарий',
                    action_obj=comment,
                    target=parent
                )

    def _get_answer(self, answer_id: int) -> QuestionAnswer:
        answer = QuestionAnswerQSBase().get_obj_by_id(answer_id)
        return answer

    def _notify_answer_user(
            self, sender: NewUser, target: QuestionAnswer, action_obj: AnswerComment
    ) -> None:
        answer_user = target.user
        if answer_user:
            notify(
                sender=sender, receiver=answer_user,
                text='прокомментировал ваш ответ на вопрос',
                target=target, action_obj=action_obj
            )

    def execute(
            self, comment: str, question_answer_id: int, parent_id: int, user: NewUser | AnonymousUser
    ) -> AnswerComment:

        answer = self._get_answer(answer_id=question_answer_id)

        comment = self._create_comment(
            comment=comment, answer=answer, parent_id=parent_id, user=user
        )
        self._notify_parsed_users(parent_id=parent_id, comment=comment, user=user)
        self._notify_answer_user(sender=user, target=answer, action_obj=comment)

        return comment
