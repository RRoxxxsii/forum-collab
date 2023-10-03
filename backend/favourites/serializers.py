from rest_framework import serializers

from favourites.models import Favourite


class FavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'
        read_only_fields = ('id', 'user', 'creation_date',)
