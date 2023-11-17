import json
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('email_confirmed', True)

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
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        'Почтовый адрес',
        unique=True,
        error_messages={'unique': 'Указаный почтовый адрес уже занято.'},
        db_index=True
    )
    user_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        error_messages={'unique': 'Указаное имя уже занято.'}
    )

    created = models.DateTimeField(default=timezone.now)
    about = models.TextField('Описание', max_length=500, blank=True)
    profile_image = models.ImageField('Аватарка', null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    # Если is_active is False, в таком случае аккаунт пользователя удален.
    is_active = models.BooleanField(default=True)
    # Время, на протяжении какого пользователь считается удаленным.
    time_deleted = models.DateTimeField(null=True, blank=True)

    # Если is_banned is True, то пользователь не имеет доступа к сайту.
    is_banned = models.BooleanField(default=False)

    # Подтвержденный почтовый адрес дает некоторые привилегии пользователю
    email_confirmed = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_name

    def get_top_expert_tags(self) -> QuerySet:
        from forum.models import ThemeTag

        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key': settings.EXPERT_TAGS_NAME})

        expert_tags = cache.get(data_cache)

        if not expert_tags:
            expert_tags = (
                ThemeTag.objects
                .filter(questions__question_answers__user=self, questions__question_answers__is_solving=True)
                .annotate(answer_count=models.Count('questions__question_answers'))
                .order_by('-answer_count')[:5]
            )
            cache.set(data_cache, expert_tags, 60)
        return expert_tags

    def get_amount_question_solved(self) -> int:
        """
        Считает количество решенных вопросов, не считая случаи, когда пользователь ответил на свой вопрос, и
        отметил ответ как решающий.
        """
        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key:': settings.QUESTION_SOLVED_NAME})

        # получаем количество ответов, которые создал пользователь по отношению к своему вопросу и оценил как решенный
        count_rated_himself = self.question_answers.filter(
            user=self,
            is_solving=True,
            question__user=self
        ).count()

        count = cache.get(data_cache)

        if not count:
            count = self.question_answers.filter(is_solving=True).count() - count_rated_himself
            cache.set(data_cache, count, 60)

        return count

    def count_question_likes(self) -> int:
        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key': settings.QUESTION_LIKE_NAME})
        count = cache.get(data_cache)

        if not count:
            count = self.questions.aggregate(
                count=Coalesce(Sum('rating__like_amount'), 0)
            ).get('count')
            cache.set(data_cache, count, 60)

        return count

    def count_question_dislikes(self) -> int:
        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key': settings.QUESTION_DISLIKE_NAME})
        count = cache.get(data_cache)

        if not count:
            count = self.questions.aggregate(
                count=Coalesce(Sum('rating__dislike_amount'), 0)
            ).get('count')
            cache.set(data_cache, count, 60)

        return count

    def count_answer_likes(self) -> int:
        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key': settings.ANSWER_LIKE_NAME})
        count = cache.get(data_cache)

        if not count:
            count = self.question_answers.aggregate(
                count=Coalesce(Sum('rating__like_amount'), 0)
            ).get('count')
            cache.set(data_cache, count, 60)

        return count

    def count_answer_dislikes(self) -> int:
        user_id = self.pk
        data_cache = json.dumps({'user_id': user_id, 'key': settings.ANSWER_DISLIKE_NAME})
        count = cache.get(data_cache)

        if not count:
            count = self.question_answers.aggregate(
                count=Coalesce(Sum('rating__dislike_amount'), 0)
            ).get('count')
            cache.set(data_cache, count, 60)

        return count

    def count_karma(self) -> int:
        """
        Карма = количество решенных пользователем вопросов * 10 + количество лайков
        вопросов + количество лайков ответов + 10 (если почта подтверждена)
        """

        karma = self.get_amount_question_solved() * 10
        if self.email_confirmed:
            karma += 10

        questions_like_amount = self.count_question_likes()
        answers_like_amount = self.count_answer_likes()
        karma += questions_like_amount
        karma += answers_like_amount

        return karma


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(
        'Токен',
        primary_key=True,
        default=uuid4,
        editable=False
    )
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
