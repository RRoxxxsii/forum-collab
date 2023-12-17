from __future__ import annotations

from accounts.models import NewUser
from django.contrib.auth.models import AnonymousUser

from .models import Notification


def notify(receiver: NewUser,
           target,
           text: [str | None] = None,
           sender: [NewUser | None] = None,
           action_obj=None,
           **kwargs):

    """
    Создание уведомления для пользователя. Возвращает булевый объект, в зависимости
    от того, было создано уведомление или нет.
    """

    if isinstance(sender, AnonymousUser):
        sender = None

    if sender != receiver:

        level = kwargs.pop('level', None)
        emailed = kwargs.pop('emailed', None)

        notification = Notification.objects.create(
            sender=sender, receiver=receiver,
            target=target, text=text
        )

        if action_obj:
            notification.action_obj = action_obj
        if level:
            notification.level = level
        if emailed:
            notification.emailed = emailed
        notification.save()


# class NotificationHelper:
#
#     def __init__(self, receiver: NewUser, target, text: [str | None] = None,
#                  sender: [NewUser | None] = None, action_obj=None, **kwargs):
#
#         self.receiver = receiver
#         self.target = target
#         self.text = text
#         self.sender = sender
#         self.action_obj = action_obj
#         self.kwargs = kwargs
#
#     def send_notification(self) -> None:
#         value = self._validate_users()
#         if value:
#             notification = Notification.objects.create(
#                 sender=self.sender, receiver=self.receiver,
#                 target=self.target, text=self.text
#             )
#
#             self._parse_kwargs(notification=notification)
#
#     def _validate_users(self) -> bool:
#         """
#         проверяем, что receiver != sender и если sender анонимен, то
#         равен None
#         """
#         if isinstance(self.sender, AnonymousUser):
#             self.sender = None
#
#         return self.receiver != self.sender
#
#     def _parse_kwargs(self, notification: Notification) -> None:
#         """
#         При наличии non-required параметров экземпляра, добавляет
#         их к экземпляру класса уведомлений.
#         """
#         level = self.kwargs.pop('level', None)
#         emailed = self.kwargs.pop('emailed', None)
#
#         if self.action_obj:
#             notification.action_obj = self.action_obj
#         if level:
#             notification.level = level
#         if emailed:
#             notification.emailed = emailed
#         notification.save()
