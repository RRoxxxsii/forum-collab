from abc import ABC, abstractmethod

from accounts.models import NewUser


class AbstractFavouriteRepository(ABC):

    @staticmethod
    @abstractmethod
    def delete_favourite(user: NewUser, question_id: int):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_favourite_exists(user: NewUser, question_id: int) -> bool:
        raise NotImplementedError


class FavouriteRepository(AbstractFavouriteRepository):

    @staticmethod
    def delete_favourite(user: NewUser, question_id: int):
        obj = user.favourites.get(question_id=question_id)
        obj.delete()

    @staticmethod
    def get_favourite_exists(user: NewUser, question_id: int) -> bool:
        return user.favourites.filter(question_id=question_id).exists()
