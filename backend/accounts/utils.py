from __future__ import annotations

from accounts.models import NewUser


def email_exists(email: str) -> bool:
    """
    Проверка на то, существует ли электронный адрес. Если да, возвращает True,
    в противном случае False.
    """
    return NewUser.objects.filter(email=email).exists()
