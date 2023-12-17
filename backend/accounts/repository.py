from abc import ABC, abstractmethod

from accounts.models import EmailConfirmationToken, NewUser
from django.utils import timezone

from . import dto


class AbstractAccountRepository(ABC):

    @staticmethod
    @abstractmethod
    def create_user(data: dto.CreateUserDTO, password: str) -> NewUser:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_email_exists(email: str) -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_token(user: NewUser) -> EmailConfirmationToken:
        raise NotImplementedError

    @staticmethod
    def get_token_exists(token_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_token(token_id: int, user_id: int) -> EmailConfirmationToken:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def set_new_email(user: NewUser, email: str) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_user_not_active(user: NewUser) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def make_user_active(user: NewUser) -> None:
        user.is_active = True
        user.time_deleted = None
        user.save()

    @staticmethod
    @abstractmethod
    def confirm_email(user: NewUser) -> None:
        raise NotImplementedError


class BaseAccountRepository(AbstractAccountRepository):

    @staticmethod
    def create_user(data: dto.CreateUserDTO, password: str) -> NewUser:
        user = NewUser.objects.create_user(
            email=data.email, user_name=data.user_name, password=data.password
        )
        return user

    @staticmethod
    def get_email_exists(email: str) -> bool:
        return NewUser.objects.filter(email=email).exists()

    @staticmethod
    def create_token(user: NewUser) -> EmailConfirmationToken:
        token = EmailConfirmationToken(user=user)
        return token

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
