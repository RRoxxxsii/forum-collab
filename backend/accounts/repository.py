from django.utils import timezone

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


class ViewsQC:

    @staticmethod
    def list_users():
        return NewUser.objects.all()
