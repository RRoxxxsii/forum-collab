from accounts.models import NewUser
from favourites.models import Favourite


class FavouriteQueryset:

    @staticmethod
    def filter_favourite_by_user(user: NewUser):
        return Favourite.objects.filter(user=user)
