from django.contrib.auth import password_validation
from django.core.validators import ValidationError
from rest_framework import serializers
from rest_framework.serializers import \
    ValidationError as SerializerValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
        password = self.validate_password(password)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserEmailSerializer(serializers.Serializer):
    """
    Сериализатор для почтового адреса пользователя.
    """
    email = serializers.EmailField()


class DummySerializer(serializers.Serializer):
    """
    Сериалзиатор-заглушка.
    """
    dummy_field = serializers.CharField(required=False, read_only=True, help_text='Поле-заглушка')


class EmailTokenObtainSerializer(TokenObtainSerializer):
    """
    Переопределенный serializer из библиотеки SIMPLE_JWT.
    """
    username_field = NewUser.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'about', 'profile_image',
                  'is_active', 'is_banned', 'email_confirmed', 'created')
        extra_kwargs = {'created': {'format': "%Y-%m-%d %H:%M:%S"}}
        read_only_fields = ('id', 'email', 'user_name', 'is_active', 'is_banned',
                            'email_confirmed', 'created')
