from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from django.db.models import QuerySet

from accounts.models import NewUser
from forum.models import (AnswerComment, Attachment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages, ThemeTag)


class AbstractLikeDislikeRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_users_liked(obj: Question | QuestionAnswer) -> QuerySet[Question | QuestionAnswer]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_users_disliked(obj: Question | QuestionAnswer) -> QuerySet[Question | QuestionAnswer]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def set_like(obj: Question | QuestionAnswer, user: NewUser) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def set_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def remove_like(obj: Question | QuestionAnswer, user: NewUser) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def remove_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        raise NotImplementedError


class AbstractQuestionRepository(ABC):

    @staticmethod
    @abstractmethod
    def create_question(
            title: str,
            content: str,
            user: NewUser,
    ) -> Question:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def add_attachments(
            parent: Question,
            attachments: list[Attachment]
    ) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def add_tags(
            tags: Iterator[ThemeTag],
            question: Question
    ) -> None:
        raise NotImplementedError


class AbstractAnswerRepository(ABC):

    @staticmethod
    @abstractmethod
    def add_attachments(
            parent: QuestionAnswer,
            attachments: list[Attachment]
    ) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_answer(
            question: Question,
            answer: str,
            user: NewUser = None
    ) -> QuestionAnswer:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def remove_is_solving_mark(answer: QuestionAnswer, question: Question):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mark_answer_as_solving(answer: QuestionAnswer, question: Question):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_solving_answer_not_solving(answer: QuestionAnswer):
        raise NotImplementedError


class AbstractCommentRepository(ABC):

    @staticmethod
    @abstractmethod
    def create_comment(
            comment: str,
            question_answer: QuestionAnswer,
            parent_id: int,
            user: NewUser
    ) -> AnswerComment:

        raise NotImplementedError


class AbsractThemeTagRepository(ABC):

    @staticmethod
    @abstractmethod
    def create_tags(
            tags: list,
            user: NewUser
    ) -> Iterator[ThemeTag]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_tag_relevant(tag: ThemeTag) -> None:
        raise NotImplementedError


class AttachmentFactory:
    @staticmethod
    def create_attachment(image, parent) -> QuestionImages | QuestionAnswerImages:
        if isinstance(parent, Question):
            return QuestionImages.objects.create(parent=parent, image=image)
        elif isinstance(parent, QuestionAnswer):
            return QuestionAnswerImages.objects.create(parent=parent, image=image)
        else:
            raise ValueError("Invalid parent type")


class BaseImageRepository:

    @staticmethod
    def add_attachments(
            parent: Question | QuestionAnswer,
            attachments: list[Attachment]
    ) -> None:
        for attachment in attachments:
            AttachmentFactory.create_attachment(image=attachment, parent=parent)


class LikeDislikeRepository(AbstractLikeDislikeRepository):

    @staticmethod
    def get_users_liked(obj: Question | QuestionAnswer) -> QuerySet[Question | QuestionAnswer]:
        return obj.rating.users_liked.all()

    @staticmethod
    def get_users_disliked(obj: Question | QuestionAnswer) -> QuerySet[Question | QuestionAnswer]:
        return obj.rating.users_disliked.all()

    @staticmethod
    def set_like(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_liked.add(user)
        obj.rating.like_amount += 1
        obj.rating.save()

    @staticmethod
    def set_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_disliked.add(user)
        obj.rating.dislike_amount += 1
        obj.rating.save()

    @staticmethod
    def remove_like(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_liked.remove(user)
        obj.rating.like_amount -= 1
        obj.rating.save()

    @staticmethod
    def remove_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_disliked.remove(user)
        obj.rating.dislike_amount -= 1
        obj.rating.save()


class ThemeTagRepository(AbsractThemeTagRepository):

    @staticmethod
    def create_tags(
            tags: list,
            user: NewUser
    ) -> Iterator[ThemeTag]:

        for tag in tags:
            tag, created = ThemeTag.objects.get_or_create(tag_name=tag, defaults={
                'is_user_tag': True,
                'is_relevant': False,
                'user': user
            })

            yield tag

    @staticmethod
    def make_tag_relevant(tag: ThemeTag) -> None:
        tag.is_relevant = True
        tag.save(update_fields=['is_relevant'])


class QuestionRepository(AbstractQuestionRepository, BaseImageRepository):

    @staticmethod
    def create_question(
            title: str, content: str, user: NewUser,
    ) -> Question:
        question = Question.objects.create(
            user=user,
            title=title,
            content=content
        )

        return question

    @staticmethod
    def add_attachments(
            parent: Question, attachments: list[Attachment]
    ) -> None:
        BaseImageRepository.add_attachments(parent, attachments)

    @staticmethod
    def add_tags(
            tags: Iterator[ThemeTag],
            question: Question
    ) -> None:
        question.tags.add(*tags)
        question.save()


class AnswerRepository(AbstractAnswerRepository, BaseImageRepository):

    @staticmethod
    def create_answer(
            question: Question,
            answer: str,
            user: NewUser = None
    ) -> QuestionAnswer:
        answer = QuestionAnswer.objects.create(question=question, answer=answer, user=user)
        return answer

    @staticmethod
    def add_attachments(
            parent: QuestionAnswer, attachments: list[Attachment]
    ) -> None:
        return BaseImageRepository.add_attachments(parent, attachments)

    @staticmethod
    def remove_is_solving_mark(answer: QuestionAnswer, question: Question):
        answer.is_solving = False
        question.is_solved = False
        answer.save()
        question.save()

    @staticmethod
    def make_solving_answer_not_solving(answer: QuestionAnswer):
        answer.is_solving = False
        answer.save()

    @staticmethod
    def mark_answer_as_solving(answer: QuestionAnswer, question: Question):
        answer.is_solving = True
        question.is_solved = True
        answer.save()
        question.save()


class CommentRepository(AbstractCommentRepository):

    @staticmethod
    def create_comment(
            comment: str,
            question_answer: QuestionAnswer,
            parent_id: int,
            user: NewUser
    ) -> AnswerComment:

        comment = AnswerComment.objects.create(
            comment=comment, question_answer=question_answer,
            user=user, parent_id=parent_id
        )

        return comment
