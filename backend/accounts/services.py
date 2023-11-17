import functools

from accounts.models import NewUser, EmailConfirmationToken
from accounts import repository
from .tasks import send_confirmation_email


class BaseRepository:
    repository = None

    @classmethod
    def get_repository(cls):
        return cls.repository


class BaseAccountService(BaseRepository):
    repository = repository.BaseAccountRepository

    @classmethod
    def create_user(cls, data: dict) -> NewUser:
        password = data.pop('password')
        instance = NewUser(**data)
        user = cls.repository.create_user(instance=instance, password=password)
        return user

    @classmethod
    def send_email(cls, user: NewUser, scheme: str, domain: str, path: str, template_name: str, request_path: str) -> None:

        instance = EmailConfirmationToken(user=user)
        token = cls.repository.create_token(instance=instance)
        current_url = cls.get_current_site(scheme=scheme, domain=domain, path=path, request_path=request_path)

        send_confirmation_email.delay(
            template_name=template_name, current_url=current_url,
            email=user.email, token_id=token.id, user_id=user.pk
        )

    @classmethod
    def get_current_site(cls, scheme: str, domain: str, path: str, request_path: str) -> str:
        """
        Возвращает путь к странице включая доменное имя и тип соединения (http или https).
        """
        path = '/'.join(str(request_path).split('/')[:-2]) + f'/{path}/'  # путь к странице без query params
        current_url = f"{scheme}://{domain}{path}"
        return current_url

    @staticmethod
    def confirm_with_email(func):
        def wrapper(view, request, *args, **kwargs):
            token_id = request.GET.get('token_id')
            user_id = request.GET.get('user_id')

            token_exists = BaseAccountService.repository.get_token_exists(token_id=token_id, user_id=user_id)

            if token_exists:
                token = BaseAccountService.repository.get_token(token_id=token_id, user_id=user_id)
                user = token.user
                return func(view, request, user, token_id=None, user_id=None, *args, **kwargs)
            return func(view, request, None, token_id=None, user_id=None, *args, **kwargs)
        return wrapper
