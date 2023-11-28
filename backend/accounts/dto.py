from typing import TypedDict

from accounts.models import NewUser


class CreateUserDTO(TypedDict):
    user_name: str
    email: str
    password: str


class RequestForConfirmationEmailDTO(TypedDict):
    user: NewUser
    request_path: str
    template_name: str
    path: str


class ConfirmByEmailDTO(TypedDict):
    token_id: int
    user_id: int
    user: NewUser


class ConfirmByEmailWithEmailDTO(ConfirmByEmailDTO):
    email: str
