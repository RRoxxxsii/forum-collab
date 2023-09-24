from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationsSerializer


class UserNotificationListAPIView(ListAPIView):
    """
    Возвращает список уведомлений для каждого аутентифицированного пользователя.
    """
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(receiver=user)
        return queryset
