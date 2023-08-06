from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmailConfirmationToken
from .permissions import EmailIsNotConfirmed
from .serializers import RegisterUserSerializer
from .utils import get_current_site, send_confirmation_email


class CustomUserRegisterAPIView(APIView):
    """
    Создания аккаунта пользователя.
    При успешном запросе: status 201
    В противном случае: status 400
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailToConfirmAPIView(APIView):
    """
    Подтверждение адреса электронной почты пользователя. Пользователь должен быть аутентифицирован.
    Возвращает сообщение о том, что письмо было отправлено и статус 201.
    Для того чтобы отправить запрос, статус пользователя email_confirmed должен быть False.
    """
    permission_classes = [IsAuthenticated, EmailIsNotConfirmed]

    def post(self, request):
        current_url = get_current_site(request, path='email-confirmation-result')   # Часть url для подтверждения

        user = request.user
        data = {'message': 'Сообщение на электронную почту отправлено. Перейдите по ссылке'
                           ' внутри письма, чтобы подтвердить почтовый адрес.'}

        # Создание токена (будет частью url-адреса) для того, чтобы в дальнейшем подтвердить эл. почту.
        token = EmailConfirmationToken.objects.get_or_create(user=user)
        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url,
                                email=user.email, token_id=token[0].pk, user_id=user.id)

        return Response(data=data, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос и статус его аккаунта email_confirmed становится положительным.
    """
    success_message = 'Почтовый адрес успешно подтвержден!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def get(self, request):
        token_id = request.GET.get('token_id', None)
        try:
            token = EmailConfirmationToken.objects.get(pk=token_id)
            user = token.user
            user.email_confirmed = True
            user.save()
            return Response({'message': self.success_message}, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': self.error_message}, status=400)
