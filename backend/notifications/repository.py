from abc import ABC, abstractmethod

from notifications.models import Notification


class AbstractNotificationsRepository(ABC):

    @staticmethod
    @abstractmethod
    def mark_notifications_as_read(list_id: list) -> None:
        raise NotImplementedError


class NotificationsRepository(AbstractNotificationsRepository):

    @staticmethod
    def mark_notifications_as_read(list_id: list) -> None:
        notifications_to_update = Notification.objects.filter(id__in=list_id)
        notifications_to_update.mark_all_as_read()
