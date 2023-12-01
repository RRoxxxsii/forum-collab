from notifications.di import container
from notifications.repository import AbstractNotificationsRepository


class MarkNotificationsAsReadService:

    def __init__(self):
        self.repo: AbstractNotificationsRepository = container.resolve(AbstractNotificationsRepository)

    def _mark_notifications_as_read(self, list_id: list) -> None:
        self.repo.mark_notifications_as_read(list_id=list_id)

    def execute(self, list_id: list) -> None:
        self._mark_notifications_as_read(list_id=list_id)
