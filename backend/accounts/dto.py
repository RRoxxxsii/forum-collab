from dataclasses import dataclass

from accounts.models import NewUser


@dataclass(frozen=True)
class CreateUserDTO:
    user_name: str
    email: str
    password: str


@dataclass(frozen=True)
class RequestForConfirmationEmailDTO:
    user: NewUser
    request_path: str
    template_name: str
    path: str


@dataclass(frozen=True)
class ConfirmByEmailDTO:
    token_id: int
    user_id: int
    user: NewUser


@dataclass(frozen=True)
class ConfirmByEmailWithEmailDTO(ConfirmByEmailDTO):
    email: str
