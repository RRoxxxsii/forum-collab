from accounts.models import NewUser
from favourites.di import container
from favourites.repository import AbstractFavouriteRepository


class FavouriteService:

    def __init__(self):
        self.repo: AbstractFavouriteRepository = container.resolve(AbstractFavouriteRepository)

    def delete_from_favourites_if_exists(self, user: NewUser, question_id: int) -> bool:
        if self.repo.get_favourite_exists(user=user, question_id=question_id):
            self.repo.delete_favourite(user=user, question_id=question_id)
            return True
        return False
