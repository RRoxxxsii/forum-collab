from __future__ import annotations

from accounts.models import NewUser


def get_current_site(request, path: str) -> str:
    """
    Возвращает путь к странице включая доменное имя и тип соединения (http или https).
    """
    scheme = request.scheme  # http или https
    domain = request.get_host()  # доменное имя
    path = '/'.join(str(request.path).split('/')[:-2]) + f'/{path}/'  # путь к странице без query params
    current_url = f"{scheme}://{domain}{path}"
    return current_url


def email_exists(email: str) -> bool:
    """
    Проверка на то, существует ли электронный адрес. Если да, возвращает True,
    в противном случае False.
    """
    return NewUser.objects.filter(email=email).exists()
