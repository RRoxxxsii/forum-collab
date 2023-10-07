from rest_framework import serializers

from accounts.serializers import UserSerializer
from favourites.models import Favourite
from forum.serializers import ListQuestionSerializer


class FavouritesSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    favourite_question = ListQuestionSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = '__all__'
        read_only_fields = ('id', 'user', 'favourite_question', 'creation_date',)
