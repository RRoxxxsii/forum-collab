from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.querysets import FavouriteQueryset
from favourites.serializers import FavouritesSerializer
from favourites.services import FavouriteService


class AddToFavouritesAPIView(CreateAPIView):
    """
    Добавление вопроса в избранное.
    Request: {'question': Number(id)}
    """
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_id = serializer.data.get('question')
        is_deleted = FavouriteService.delete_from_favourites_if_exists(
            user=request.user, question_id=question_id
        )
        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        serializer.save(user=user)


class FavouritesListAPIView(ListAPIView):
    """
    Список избранных вопросов для пользователя.
    """
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return FavouriteQueryset.filter_favourite_by_user(self.request.user)

