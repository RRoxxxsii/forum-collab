from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmailConfirmationToken
from .serializers import RegisterUserSerializer
from .utils import send_confirmation_email


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
    Подтверждение адреса электронной почты пользователя.
    Пользователь должен быть аутентифицирован.
    Возвращает сообщение о том, что письмо было отправлено и статус 201.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        scheme = request.scheme  # http или https
        domain = request.get_host()  # доменное имя
        path = request.path  # путь к странице без query params
        current_url = f"{scheme}://{domain}{path}"

        user = request.user
        data = {'message': 'Сообщение на электронную почту отправлено. Перейдите по ссылке'
                           'внутри письма, чтобы подтвердить почтовый адрес.'}

        token = EmailConfirmationToken.objects.get_or_create(user=user)
        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url,
                                email=user.email, token_id=token[0].pk, user_id=user.id)

        return Response(data=data, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView:

    pass
