from __future__ import annotations

from datetime import datetime

from django.db.models import (Count, ExpressionWrapper, F, IntegerField,
                              QuerySet)

from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag


class ObjQSBase:
    obj_type = None

    @classmethod
    def get_obj_list(cls, offset: int = None, limit: int = None) -> QuerySet:
        if cls.obj_type and (not offset and offset != 0 and not limit):
            return cls.obj_type.objects.all()
        if cls.obj_type and (offset or offset == 0 and limit):
            return cls.obj_type.objects.all()[offset:limit]

    @classmethod
    def get_obj_by_id(cls, obj_id: int):
        if cls.obj_type:
            return cls.obj_type.objects.get(id=obj_id)


class QuestionQSBase(ObjQSBase):
    obj_type = Question

    def filter_solving_answers(self, question: Question) -> bool:
        return question.question_answers.filter(is_solving=True).exists()

    def get_solving_answer(self, question: Question) -> QuestionAnswer:
        return question.question_answers.get(is_solving=True)


class QuestionAnswerQSBase(ObjQSBase):
    obj_type = QuestionAnswer


class CommentQSBase(ObjQSBase):
    obj_type = AnswerComment


class ThemeTagQSBase(ObjQSBase):

    @classmethod
    def get_most_popular_tags(cls):
        return ThemeTag.objects.annotate(use_amount=Count('questions')).order_by('-use_amount')[:20]

    @staticmethod
    def get_tags(tag) -> QuerySet[ThemeTag | None]:
        return ThemeTag.objects.filter(tag_name__icontains=tag).order_by('is_user_tag')


class QuestionQS(QuestionQSBase):

    @classmethod
    def question_list_ordered(cls, field: str) -> QuerySet:
        return Question.objects.all().order_by(field)

    @classmethod
    def question_list_filtered_by_solving_ordered_with_limit(
            cls,
            is_solved: bool,
            field: str,
            offset: int,
            limit: int
    ) -> QuerySet:
        return Question.objects.filter(is_solved=is_solved).order_by(field)[offset:limit]

    @classmethod
    def question_list_ordered_by_best(
            cls,
            amount_of_questions: int,
            time_period: datetime
    ) -> QuerySet:
        questions = Question.objects.annotate(
            answer_count=Count('question_answers'),
            comment_count=Count('question_answers__answer_comments'),
            like_count=Count('rating__users_liked'),
            dislike_count=Count('rating__users_disliked'),
            score=ExpressionWrapper(
                F('like_count') + F('answer_count') * 2 +
                F('comment_count') - F('dislike_count') * 0.5,
                output_field=IntegerField()
            )
        ).filter(creation_date__gte=time_period).order_by('-score', '-creation_date')[:amount_of_questions]
        return questions
