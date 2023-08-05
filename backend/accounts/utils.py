from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(template_name: str, current_url: str, email: str, token_id: int, user_id: int):
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
