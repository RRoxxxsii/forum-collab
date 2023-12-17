import punq
from accounts.repository import (AbstractAccountRepository,
                                 BaseAccountRepository)

container = punq.Container()
container.register(AbstractAccountRepository, BaseAccountRepository)
