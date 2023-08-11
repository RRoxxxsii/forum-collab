from django.contrib.auth import password_validation
from django.core.validators import ValidationError
from rest_framework import serializers
from rest_framework.serializers import \
    ValidationError as SerializerValidationError

from .models import NewUser


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        try:
            password_validation.validate_password(password=password)
        except ValidationError as err:
            raise SerializerValidationError(str(err))
        return password

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password = self.validate_password(password)  # Call the custom validation method
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class DummySerializer(serializers.Serializer):
    """
    Сериалзиатор-заглушка.
    """
    dummy_field = serializers.CharField(required=False, read_only=True, help_text='Поле-заглушка')
