from accounts.models import NewUser


class FavouritesRepository:

    @staticmethod
    def get_favourite_exists(user: NewUser, question_id: int) -> bool:
        return user.favourites.filter(question_id=question_id).exists()

    @staticmethod
    def delete_favourite(user: NewUser, question_id: int):
        obj = user.favourites.get(question_id=question_id)
        obj.delete()
