from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен быть is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен быть is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('Необходимо предоставить адрес электронной почты')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    user_name = models.CharField(max_length=150, unique=True)

    created = models.DateTimeField(default=timezone.now)
    about = models.TextField(verbose_name='Описание', max_length=500, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_name


