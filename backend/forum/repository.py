from __future__ import annotations

from typing import Iterator

from django.db.models import QuerySet

from accounts.models import NewUser
from forum.models import Question, QuestionAnswer, QuestionImages, QuestionAnswerImages, ThemeTag, Attachment


class ThemeTagRepository:

    @staticmethod
    def create_tags(
            tags: list,
            user: NewUser
    ) -> Iterator[ThemeTag]:
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


class AnswerRepository(BaseImageRepository):

    @staticmethod
    def create_answer(
            question: Question,
            answer: str,
            user: NewUser = None
    ) -> QuestionAnswer:
        answer = QuestionAnswer.objects.create(question=question, answer=answer, user=user)
        return answer
