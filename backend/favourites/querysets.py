from accounts.models import NewUser
from django.db.models import QuerySet
from favourites.models import Favourite


class FavouriteQueryset:

    @staticmethod
    def filter_favourite_by_user(user: NewUser) -> QuerySet[Favourite]:
        return Favourite.objects.filter(user=user)

    @staticmethod
    def get_favourite_exists(user: NewUser, question_id: int) -> bool:
        return user.favourites.filter(question_id=question_id).exists()
