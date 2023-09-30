from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .helpers import BaseEmailConfirmAPIView
from .models import EmailConfirmationToken, NewUser
from .permissions import EmailIsNotConfirmed
from .serializers import (CustomTokenObtainPairSerializer, DummySerializer,
                          RegisterUserSerializer, UserEmailSerializer,
                          UserSerializer)
from .utils import email_exists, get_current_site, send_confirmation_email


class CustomUserRegisterAPIView(GenericAPIView):
    """
    Создания аккаунта пользователя.
    При успешном запросе: status 201 и success message; В противном случае: status 400 и error message.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    success_message = 'Вы успешно создали аккаунт!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)
        return Response(data={"message": self.error_message}, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailToConfirmAPIView(GenericAPIView):
    """
    Подтверждение адреса электронной почты пользователя. Право отправить запрос имеет пользователь, чей
    стаутс email_confirmed=False.
    При успешном запросе: status 201 и success message; В противном случае: status 400 и error message.
    """
    permission_classes = [IsAuthenticated, EmailIsNotConfirmed]
    success_message = 'Сообщение на электронную почту отправлено. Перейдите по ссылке ' \
                      'внутри письма, чтобы подтвердить почтовый адрес.'
    serializer_class = DummySerializer

    def get(self, request):
        current_url = get_current_site(request, path='email-confirmation-result')   # Часть url для подтверждения

        user = request.user

        # Создание токена (будет частью url-адреса) для того, чтобы в дальнейшем подтвердить эл. почту.
        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url,
                                email=user.email, token_id=token.id, user_id=user.id)

        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(BaseEmailConfirmAPIView):
    """
    Пользователь отправляет GET запрос на url-адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Почтовый адрес успешно подтвержден!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def perform_action(self, user):
        user.email_confirmed = True
        user.save()


class ChangeEmailAddressAPIView(GenericAPIView):
    """
    Запрос пользователя на смену почтового адреса. Входные данные - новый почтовый адрес.
    При успешном запросе: status 201 и success message; В противном случае: status 400 и error message.
    """
    serializer_class = UserEmailSerializer
    permission_classes = [IsAuthenticated, ]
    success_message = 'Сообщение на почту отправлено. Подтвердите электронный адрес, чтобы изменить почтовый адрес.'
    error_message = 'Пользователь с таким почтовым адресом уже существует.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = request.user
        # Проверка на то, существует ли такой адрес в БД.
        if email_exists(email):
            return Response(data={"message": self.error_message},
                            status=status.HTTP_400_BAD_REQUEST)

        request.session['email'] = email
        current_url = get_current_site(request, path='new-email-confirmation-result')   # Часть url для подтверждения

        # Создаем новый токен
        token = EmailConfirmationToken.objects.create(user=user)

        send_confirmation_email(template_name='email/confirm_email.txt', current_url=current_url, email=email,
                                token_id=token.id, user_id=user.id)

        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmNewEmailAPIView(BaseEmailConfirmAPIView):
    """
    Пользователь отправляет GET запрос на адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно поменяли адрес электронной почты!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'
    permission_classes = [IsAuthenticated, ]

    def perform_action(self, user):
        email = self.request.session.get('email')
        user.email = email
        user.save()


class DeleteAccountAPIView(GenericAPIView):
    """
    GET-запрос - аккаунт пользователя удаляется(is_active=False), но остается в БД.
    При успешном выполнении возвращается код статуса 200 и success_message.
    """
    permission_classes = [IsAuthenticated, ]
    success_message = 'Аккаунт удален. Вы можете восстановить его в течение 6 месяцев '
    serializer_class = DummySerializer

    def get(self, request):
        user = request.user
        user.is_active = False
        user.time_deleted = timezone.now()
        user.save()

        return Response(data={"message": self.success_message}, status=status.HTTP_200_OK)


class RestoreAccountAPIView(GenericAPIView):
    """
    Восстановление аккаунта.
    Возвращает статус 201 и success_message если успешно;
    В противном случае 400 и error_message.
    """
    serializer_class = UserEmailSerializer
    success_message = 'Сообщение на почту отправлено. Подтвердите электронный адрес, чтобы восстановить аккаунт.'
    error_message = 'Введенный вами адрес электронной почты недействителен.'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = request.user
        # Проверка на то, существует ли такой адрес в БД и активен ли пользователь.
        if not email_exists(email) or user.is_active:
            return Response(data={"message": self.error_message},
                            status=status.HTTP_400_BAD_REQUEST)
        elif user.email == email:
            # Создаем новый токен
            token = EmailConfirmationToken.objects.create(user=user)
            current_url = get_current_site(request=request, path='restore-account-email-confirm')
            send_confirmation_email(template_name='email/restore_account.txt', email=email, user_id=user.id,
                                    current_url=current_url, token_id=token.id)

            return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)
        # В случае, если что-то пошло не так
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RestoreAccountFromEmailAPIView(BaseEmailConfirmAPIView):
    """
    GET запрос на адрес, полученный в почтовом сообщении - восстановление аккаунта (is_active=True).
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно восстановили свой аккаунт!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def perform_action(self, user):
        user.is_active = True
        user.time_deleted = None
        user.save()


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    На вход принимает пароль и почтовый адрес пользователя. Возвращает access и refresh_token.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', )


class UploadProfileImageAPIView(UpdateAPIView):
    pass

