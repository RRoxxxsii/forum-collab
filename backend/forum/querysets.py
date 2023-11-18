from django.db.models import QuerySet

from forum.models import Question, QuestionAnswer, AnswerComment


class QuestionQS:

    @staticmethod
    def question_list() -> QuerySet[Question]:
        return Question.objects.all()


class QuestionAnswerQS:

    @staticmethod
    def answer_list() -> QuerySet[QuestionAnswer]:
        return QuestionAnswer.objects.all()


class CommentQS:

    @staticmethod
    def comment_list() -> QuerySet[AnswerComment]:
        return AnswerComment.objects.all()