from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmailConfirmationToken
from .permissions import EmailIsNotConfirmed
from .serializers import EmailSerializer, RegisterUserSerializer
from .utils import (check_email_exists, get_current_site,
                    send_confirmation_email)


class CustomUserRegisterAPIView(APIView):
    """
    Создания аккаунта пользователя.
    При успешном запросе: status 201
    В противном случае: status 400
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestEmailToConfirmAPIView(APIView):
    """
    Подтверждение адреса электронной почты пользователя. Пользователь должен быть аутентифицирован.
    Возвращает сообщение о том, что письмо было отправлено и статус 201.
    Для того чтобы отправить запрос, статус пользователя email_confirmed должен быть False.
    """
    permission_classes = [IsAuthenticated, EmailIsNotConfirmed]

    def get(self, request):
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
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated, ]
    success_message = 'Сообщение на почту отправлено. Подтвердите электронный адрес, чтобы изменить почтовый адрес.'
    error_message = 'Пользователь с таким почтовым адресом уже существует.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # Проверка на то, существует ли такой адрес в БД.
        if check_email_exists(email):
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
    permission_classes = [IsAuthenticated, ]

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


class DeleteAccountAPIView(APIView):
    """
    Удаление аккаунта. Пользователь отправляет GET-запрос на url и при успешном запросе
    его аккаунт 'удаляется' (остается в БД в течение определенного времени, но до процедуры
    восстановления пользователь не имеет доступ).
    При переходе по запросу аккаунт становится is_active=False.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data=
        {'message': 'Аккаунт удален. Вы можете восстановить его в течение двух '},
        status=status.HTTP_200_OK)


class RestoreAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer
    success_message = 'Сообщение на почту отправлено. Подтвердите электронный адрес, чтобы восстановить аккаунт.'
    error_message = 'Введенный вами адрес электронной почты недействителен.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = request.user
        # Проверка на то, существует ли такой адрес в БД и активен ли пользователь.
        if not check_email_exists(email) or user.is_active:
            return Response(data={'message': self.error_message}, status=status.HTTP_400_BAD_REQUEST)
        elif user.email == email:
            # Создаем новый токен
            token = EmailConfirmationToken.objects.create(user=user)
            current_url = get_current_site(request=request, path='restore-account-email-confirm')
            send_confirmation_email(template_name='email/restore_account.txt', email=email, user_id=user.id,
                                    current_url=current_url, token_id=token.id)

            return Response(data={'message': self.success_message}, status=status.HTTP_200_OK)
        # В случае, если что-то пошло не так
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RestoreAccountFromEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос и его аккаунт восстанавливается;
    статус его аккаунта is_active становится положительным.
    GET запрос отправляется на url-адрес, полученный в почтовом сообщении.
    """
    success_message = 'Вы успешно восстановили свой аккаунт!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def get(self, request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)
        try:
            token = EmailConfirmationToken.objects.get(id=token_id, user=user_id)
            user = token.user
            user.is_active = True
            user.save()
            return Response({'message': self.success_message}, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': self.error_message}, status=400)


