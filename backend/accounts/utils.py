from django.core.mail import send_mail
from django.template.loader import get_template

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


def send_confirmation_email(template_name: str, current_url: str, email: str, token_id: int, user_id: int):
    """
    Отправляет письмо для подтверждения определенных действий.
    """
    data = {
        'current_site': str(current_url),
        'token_id': str(token_id),
        'user_id': str(user_id)
    }
    message = get_template(template_name).render(data)
    send_mail(subject='Пожалуйста, подтвердите почту',
              message=message,
              from_email='admin@ourweb.com',
              recipient_list=[email],
              fail_silently=True)


def email_exists(email: str) -> bool:
    """
    Проверка на то, существует ли электронный адрес. Если да, возвращает True,
    в противном случае False.
    """
    return NewUser.objects.filter(email=email).exists()
