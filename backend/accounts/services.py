from accounts.models import NewUser

from . import dto
from .di import container
from .repository import AbstractAccountRepository
from .tasks import send_confirmation_email


class CreateUserService:

    def __init__(self):
        self.repo: AbstractAccountRepository = container.resolve(AbstractAccountRepository)

    def _create_user(self, data: dto.CreateUserDTO) -> NewUser:
        password = data.password
        user = self.repo.create_user(data=data, password=password)
        return user

    def execute(self, data: dto.CreateUserDTO):
        return self._create_user(data)


class SendConfirmationEmailService:

    def __init__(self):
        self.repo: AbstractAccountRepository = container.resolve(AbstractAccountRepository)

    def _send_confirmation_email(self, data: dto.RequestForConfirmationEmailDTO):
        user = data.user
        token = self.repo.create_token(user)

        current_url = '/'.join(data.request_path.split('/')[:-2]) + f"/{data.path}"

        send_confirmation_email.delay(
            template_name=data.template_name, current_url=current_url,
            email=user.email, token_id=token.id, user_id=user.pk
        )

    def execute(self, data: dto.RequestForConfirmationEmailDTO):
        return self._send_confirmation_email(data)


class ConfirmWithEmailService:

    def __init__(self):
        self.repo: AbstractAccountRepository = container.resolve(AbstractAccountRepository)

    def confirm_with_email(self, func):
        def wrapper(*args, **kwargs):
            token_id = kwargs.get('token_id')
            user_id = kwargs.get('user_id')
            token_exists = self.repo.get_token_exists(token_id=token_id, user_id=user_id)

            if token_exists:
                self.repo.get_token(token_id=token_id, user_id=user_id)

                return func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper


class PerformActionWhenConfirm:
    def __init__(self):
        self.repo: AbstractAccountRepository = container.resolve(AbstractAccountRepository)

    @ConfirmWithEmailService().confirm_with_email
    def confirm_email(self, data: dto.ConfirmByEmailDTO):
        user = data.user
        if isinstance(user, NewUser):
            self.repo.confirm_email(user)
            return True
        return False

    @ConfirmWithEmailService().confirm_with_email
    def make_user_active(self, data: dto.ConfirmByEmailDTO):
        user = data.user
        if isinstance(user, NewUser):
            self.repo.make_user_active(user)
            return True
        return False

    @ConfirmWithEmailService().confirm_with_email
    def set_new_email(self, data: dto.ConfirmByEmailWithEmailDTO):
        user = data.user
        email = data.email
        if isinstance(user, NewUser):
            self.repo.set_new_email(user, email)
            return True
        return False
