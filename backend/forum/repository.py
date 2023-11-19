from __future__ import annotations

from typing import Iterator

from django.db.models import QuerySet

from accounts.models import NewUser
from forum.models import Question, QuestionAnswer, QuestionImages, QuestionAnswerImages, ThemeTag, Attachment, \
    AnswerComment
from forum.querysets import ObjQSBase


class LikeDislikeRepository:

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

    @staticmethod
    def set_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_disliked.add(user)
        obj.rating.dislike_amount += 1

    @staticmethod
    def remove_like(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_liked.remove(user)
        obj.rating.like_amount -= 1

    @staticmethod
    def remove_dislike(obj: Question | QuestionAnswer, user: NewUser) -> None:
        obj.rating.users_disliked.remove(user)
        obj.rating.dislike_amount -= 1


class ThemeTagRepository:

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
    def get_tags(tag) -> QuerySet[ThemeTag | None]:
        return ThemeTag.objects.filter(tag_name__icontains=tag).order_by('is_user_tag')


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


class QuestionRepository(BaseImageRepository):

    @staticmethod
    def create_question(
            title: str,
            content: str,
            user: NewUser,
    ) -> Question:
        question = Question.objects.create(
            user=user,
            title=title,
            content=content
        )

        return question

    @staticmethod
    def add_tags(
            tags: Iterator[ThemeTag],
            question: Question
    ) -> None:
        question.tags.add(*tags)
        question.save()


class AnswerRepository(BaseImageRepository, ObjQSBase):

    @staticmethod
    def create_answer(
            question: Question,
            answer: str,
            user: NewUser = None
    ) -> QuestionAnswer:
        answer = QuestionAnswer.objects.create(question=question, answer=answer, user=user)
        return answer


class CommentRepository(ObjQSBase):

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
