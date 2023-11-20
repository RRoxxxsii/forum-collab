from accounts.models import NewUser


class ObjQSBase:
    obj_type = None

    @classmethod
    def get_obj_list(cls):
        if cls.obj_type:
            return cls.obj_type.objects.all()

    @classmethod
    def get_obj_by_id(cls, obj_id: int):
        if cls.obj_type:
            return cls.obj_type.objects.get(id=obj_id)


class UsersQS(ObjQSBase):
    obj_type = NewUser
