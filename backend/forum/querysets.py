from django.db.models import QuerySet

from forum.models import Question, QuestionAnswer


class QuestionQS:

    @staticmethod
    def question_list() -> QuerySet[Question]:
        return Question.objects.all()


class QuestionAnswerQS:

    @staticmethod
    def answer_list() -> QuerySet[QuestionAnswer]:
        return QuestionAnswer.objects.all()