from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.models import Favourite
from favourites.serializers import FavouritesSerializer


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
        user = request.user
        if user.favourites.filter(question_id=question_id).exists():
            obj = user.favourites.get(question_id=question_id)
            obj.delete()
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
        user = self.request.user
        qs = Favourite.objects.filter(user=user)
        return qs

