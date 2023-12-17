from accounts.models import NewUser
from django.db.models import QuerySet
from notifications.models import Notification


class NotificationQuerySet:

    @staticmethod
    def filter_notifications_by_user(user: NewUser) -> QuerySet[Notification]:
        return Notification.objects.filter(receiver=user)[:50]

    @staticmethod
    def get_all():
        return Notification.objects.all()
