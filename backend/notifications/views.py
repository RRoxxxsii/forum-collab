from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .querysets import NotificationQuerySet
from .serializers import NotificationsSerializer


class UserNotificationListAPIView(ListAPIView):
    """
    Возвращает список уведомлений для каждого аутентифицированного пользователя.
    """
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationQuerySet.filter_notifications_by_user(self.request.user)
