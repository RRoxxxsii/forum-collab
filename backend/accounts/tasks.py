from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_confirmation_email(template_name: str, current_url: str, email: str, token_id: int, user_id: int):
    """
    Отправляет письмо для подтверждения определенных действий.
    """
    data = {
        'current_site': str(current_url),
        'token_id': str(token_id),
        'user_id': str(user_id)
    }

    message = render_to_string(template_name, context=data)
    send_mail(
        subject='Пожалуйста, подтвердите почту',
        message=message,
        from_email='admin@ourweb.com',
        recipient_list=[email],
        fail_silently=True
    )
