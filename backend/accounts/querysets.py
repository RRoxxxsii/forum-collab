from django.db.models import QuerySet

from accounts.models import NewUser


class ObjQSBase:
    @staticmethod
    def get_obj_list(obj_type):
        return obj_type.objects.all()

    @staticmethod
    def get_obj_by_id(obj_type, obj_id: int):
        return obj_type.objects.filter(id=obj_id)


class UsersQS(ObjQSBase):
    pass
