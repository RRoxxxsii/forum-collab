import punq

from favourites.repository import (AbstractFavouriteRepository,
                                   FavouriteRepository)

container = punq.Container()

container.register(AbstractFavouriteRepository, FavouriteRepository)
