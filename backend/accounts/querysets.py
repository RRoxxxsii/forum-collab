from django.db.models import QuerySet

from accounts.models import NewUser


class ViewsQS:

    @staticmethod
    def list_users() -> QuerySet[NewUser]:
        return NewUser.objects.all()
