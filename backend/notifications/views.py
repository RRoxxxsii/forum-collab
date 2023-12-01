from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .querysets import NotificationQuerySet
from .serializers import NotificationListIDSerializer, NotificationsSerializer
from .services import MarkNotificationsAsReadService


class UserNotificationListAPIView(ListAPIView):
    """
    Возвращает список уведомлений для каждого аутентифицированного пользователя.
    """
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'get']

    def get_queryset(self):
        return NotificationQuerySet.filter_notifications_by_user(self.request.user)


class MarkNotificationsAsReadAPIView(GenericAPIView):
    """
    Принимает массив состоящий из id уведомлений и отмечает
    уведомления с указанными ID как прочитанные.
    """
    serializer_class = NotificationListIDSerializer
    queryset = NotificationQuerySet.get_all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_id = serializer.data.get('list_id')
        MarkNotificationsAsReadService().execute(list_id=list_id)
        return Response(data={'message': 'notifications were marked as read'}, status=status.HTTP_200_OK)
