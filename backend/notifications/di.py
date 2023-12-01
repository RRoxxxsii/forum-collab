import punq

from notifications.repository import (AbstractNotificationsRepository,
                                      NotificationsRepository)

container = punq.Container()
container.register(AbstractNotificationsRepository, NotificationsRepository)
