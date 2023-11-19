from django.db.models import QuerySet

from forum.models import Question, QuestionAnswer, AnswerComment


class ObjQSBase:
    @staticmethod
    def get_obj_list(obj_type):
        return obj_type.objects.all()

    @staticmethod
    def get_obj_by_id(obj_type, obj_id: int):
        return obj_type.objects.get(id=obj_id)


class QuestionQS(ObjQSBase):
    pass


class QuestionAnswerQSBase(ObjQSBase):
    pass


class CommentQSBase(ObjQSBase):
    pass

