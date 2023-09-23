from __future__ import annotations

from accounts.models import NewUser

from .models import Notification


def notify(receiver: NewUser,
           target,
           text: [str | None] = None,
           sender: [NewUser | None] = None,
           action_obj=None,
           **kwargs) -> bool:

    """
    Создание уведомления для пользователя. Возвращает булевый объект, в зависимости
    от того, было создано уведомление или нет.
    """

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

        return True
    return False
