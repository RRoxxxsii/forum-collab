from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmailConfirmationToken, NewUser
from .permissions import EmailIsNotConfirmed
from .serializers import ChangeEmailSerializer, RegisterUserSerializer
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
        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url,
                                email=user.email, token_id=token.id, user_id=user.id)

        return Response(data=data, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос и статус его аккаунта email_confirmed становится положительным.
    GET запрос отправляется на url-адрес, полученный в почтовом сообщении.
    """
    success_message = 'Почтовый адрес успешно подтвержден!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def get(self, request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)
        try:
            token = EmailConfirmationToken.objects.get(id=token_id, user=user_id)
            user = token.user
            user.email_confirmed = True
            user.save()
            return Response({'message': self.success_message}, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': self.error_message}, status=400)


class ChangeEmailAddressAPIView(APIView):
    """
    Запрос пользователя на смену почтового адреса. Входные данные - новый почтовый адрес.
    """
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated, ]
    success_message = 'Сообщение на почту отправлено. Подтвердите электронный адрес, чтобы восстановить аккаунт.'
    error_message = 'Пользователь с таким почтовым адресом уже существует.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # Проверка на то, существует ли такой адрес в БД.
        email_exists = True
        try:
            NewUser.objects.get(email=email)
        except NewUser.DoesNotExist:
            email_exists = False
        if email_exists:
            return Response(data={'message': self.error_message}, status=status.HTTP_400_BAD_REQUEST)

        request.session['email'] = email
        current_url = get_current_site(request, path='new-email-confirmation-result')   # Часть url для подтверждения
        user = request.user

        # Создаем новый токен
        token = EmailConfirmationToken.objects.create(user=user)

        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url, email=email,
                                token_id=token.id, user_id=user.id)

        return Response(data={'message': self.success_message})


class ConfirmNewEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос и ему присваивается новый почтовый адрес;
    статус его аккаунта email_confirmed становится положительным.
    GET запрос отправляется на url-адрес, полученный в почтовом сообщении.
    """
    success_message = 'Вы успешно поменяли адрес электронной почты!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def get(self, request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)
        try:
            token = EmailConfirmationToken.objects.get(id=token_id, user=user_id)
            user = token.user
            email = request.session.get('email')
            user.email = email
            user.save()
            return Response({'message': self.success_message}, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': self.error_message}, status=400)
