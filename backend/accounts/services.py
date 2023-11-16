from accounts.models import NewUser, EmailConfirmationToken
from accounts import repository
from .tasks import send_confirmation_email


class BaseRepository:
    repository = None

    @classmethod
    def get_repository(cls):
        return cls.repository


class CreateAccountService(BaseRepository):
    repository = repository.CreateAccountRepository

    @classmethod
    def create_user(cls, data: dict) -> NewUser:
        password = data.pop('password')
        instance = NewUser(**data)
        user = cls.repository.create_user(instance=instance, password=password)
        return user


class CreateTokenService(BaseRepository):
    repository = repository.CreateTokenRepository

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
