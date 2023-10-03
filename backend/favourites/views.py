from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.models import Favourite
from favourites.serializers import FavouritesSerializer


class AddToFavouritesAPIView(CreateAPIView):
    """
    Добавление вопроса в избранное.
    """
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        serializer.save(user=user)
