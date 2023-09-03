from accounts.models import NewUser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from forum.permissions import IsOwner


class UpdateDestroyRetrieveMixin(GenericAPIView, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    """
    Миксин для обновления, удаления и получения.
    """
    permission_classes = [IsOwner, IsAuthenticatedOrReadOnly]
    allowed_methods = ['PUT', 'DELETE', 'GET']

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class LikeDislikeModelMixin:
    """
    Миксин для создания функционала лайк/дизлайк.
    """
    def like(self, user: NewUser):
        # если у пользователя не стоит лайк
        if user not in self.rating.users_liked.all():
            # если у пользователя не стоит дизлайк
            if user not in self.rating.users_disliked.all():
                # ставим лайк
                self.rating.users_liked.add(user)
                self.rating.like_amount += 1
            # если у пользователя стоит дизлайк
            else:
                # убираем дизлайк
                self.rating.users_disliked.remove(user)
                self.rating.dislike_amount -= 1
                # ставим лайк
                self.rating.users_liked.add(user)
                self.rating.like_amount += 1

        # если у пользователя уже стоит лайк
        else:
            # убираем лайк
            self.rating.users_liked.remove(user)
            self.rating.like_amount -= 1

        self.rating.save()

    def dislike(self, user: NewUser):
        # если у пользователя не стоит дизлайк
        if user not in self.rating.users_disliked.all():
            # если у пользователя не стоит лайк
            if user not in self.rating.users_liked.all():
                # ставим дизлайк
                self.rating.users_disliked.add(user)
                self.rating.dislike_amount += 1
            # если у пользователя стоит лайк
            else:
                # убираем лайк
                self.rating.users_liked.remove(user)
                self.rating.like_amount -= 1
                # ставим дизлайк
                self.rating.users_disliked.add(user)
                self.rating.dislike_amount += 1

        # если у пользователя уже стоит дизлайк
        else:
            # убираем дизлайк
            self.rating.users_disliked.remove(user)
            self.rating.dislike_amount -= 1

        self.rating.save()
