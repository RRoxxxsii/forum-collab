from django.db.models import QuerySet

from accounts.models import NewUser
from notifications.models import Notification


class NotificationQuerySet:

    @staticmethod
    def filter_notifications_by_user(user: NewUser) -> QuerySet[Notification]:
        return Notification.objects.filter(receiver=user)