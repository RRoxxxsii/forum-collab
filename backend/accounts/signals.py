from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Работа с токенами сброса пароля
    При создании токена пользователю должно быть отправлено электронное письмо.
    """

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.user_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # Рендерит контекст для сообщения
    email_plain_text = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # Заголовок:
        "Password Reset for {title}".format(title="Your Website Title"),
        # Сообщение:
        email_plain_text,
        # От:
        "noreply@yourdomain.com",
        # Кому:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_plain_text, "text/html")
    msg.send()
