from accounts.models import NewUser
from favourites.repository import FavouritesRepository


class FavouriteService:
    favourite_repository = FavouritesRepository

    @classmethod
    def delete_from_favourites_if_exists(cls, user: NewUser, question_id: int) -> bool:
        if cls.favourite_repository.get_favourite_exists(user=user, question_id=question_id):
            cls.favourite_repository.delete_favourite(user=user, question_id=question_id)
            return True
        return False
