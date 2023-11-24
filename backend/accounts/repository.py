from django.conf import settings
from django.db.models import Count, QuerySet, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from accounts.cache_manager import CacheManager
from accounts.models import EmailConfirmationToken, NewUser


class BaseAccountRepository:

    @staticmethod
    def create_user(instance: NewUser, password: str) -> NewUser:
        instance.set_password(password)
        instance.save()
        return instance

    @staticmethod
    def get_email_exists(email: str) -> bool:
        return NewUser.objects.filter(email=email).exists()

    @staticmethod
    def create_token(instance: EmailConfirmationToken) -> EmailConfirmationToken:
        instance.save()
        return instance

    @staticmethod
    def get_token_exists(token_id: int, user_id: int) -> bool:
        return EmailConfirmationToken.objects.filter(id=token_id, user=user_id).exists()

    @staticmethod
    def get_token(token_id: int, user_id: int) -> EmailConfirmationToken:
        return EmailConfirmationToken.objects.get(id=token_id, user=user_id)

    @staticmethod
    def set_new_email(user: NewUser, email: str) -> None:
        user.email = email
        user.save()

    @staticmethod
    def make_user_not_active(user: NewUser) -> None:
        user.is_active = False
        user.time_deleted = timezone.now()
        user.save()

    @staticmethod
    def make_user_active(user: NewUser) -> None:
        user.is_active = True
        user.time_deleted = None
        user.save()

    @staticmethod
    def confirm_email(user: NewUser) -> None:
        user.email_confirmed = True
        user.save()


class UserKarmaQS:

    @classmethod
    @CacheManager.cache_data(key_prefix=settings.EXPERT_TAGS_NAME)
    def get_top_expert_tags(cls, user) -> QuerySet:
        from forum.models import ThemeTag

        expert_tags = (
            ThemeTag.objects
            .filter(questions__question_answers__user=user, questions__question_answers__is_solving=True)
            .annotate(answer_count=Count('questions__question_answers'))
            .order_by('-answer_count')[:5]
        )
        return expert_tags

    @classmethod
    @CacheManager.cache_data(key_prefix=settings.QUESTION_SOLVED_NAME, time=3600)
    def get_amount_question_solved(cls, user) -> int:
        """
        Считает количество решенных вопросов, не считая случаи, когда пользователь ответил на свой вопрос, и
        отметил ответ как решающий.
        """
        # получаем количество ответов, которые создал пользователь по отношению к своему вопросу и оценил как решенный
        count_rated_himself = user.question_answers.filter(
            user=user,
            is_solving=True,
            question__user=user
        ).count()

        # кол-во ответов, которые создал пользователь всего
        count = user.question_answers.filter(is_solving=True).count() - count_rated_himself

        return count

    @classmethod
    def count_question_likes(cls, user) -> int:
        count = user.questions.aggregate(
            count=Coalesce(Sum('rating__like_amount'), 0)
        ).get('count')

        return count

    @classmethod
    def count_question_dislikes(cls, user) -> int:
        count = user.questions.aggregate(
            count=Coalesce(Sum('rating__dislike_amount'), 0)
        ).get('count')

        return count

    @classmethod
    def count_answer_likes(cls, user) -> int:

        count = user.question_answers.aggregate(
            count=Coalesce(Sum('rating__like_amount'), 0)
        ).get('count')

        return count

    @classmethod
    def count_answer_dislikes(cls, user) -> int:

        count = user.question_answers.aggregate(
            count=Coalesce(Sum('rating__dislike_amount'), 0)
        ).get('count')

        return count

    @classmethod
    def count_karma(cls, user) -> int:
        """
        Карма = количество решенных пользователем вопросов * 10 + количество лайков
        вопросов + количество лайков ответов + 10 (если почта подтверждена)
        """

        karma = cls.get_amount_question_solved(user) * 10
        if user.email_confirmed:
            karma += 10

        questions_like_amount = cls.count_question_likes(user)
        answers_like_amount = cls.count_answer_likes(user)
        karma += questions_like_amount
        karma += answers_like_amount

        return karma

