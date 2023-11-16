from accounts.models import NewUser, EmailConfirmationToken


class CreateAccountRepository:

    @staticmethod
    def create_user(instance: NewUser, password: str) -> NewUser:

        instance.set_password(password)
        instance.save()

        return instance


class CreateTokenRepository:

    @staticmethod
    def create_token(instance: EmailConfirmationToken):
        instance.save()
        return instance
