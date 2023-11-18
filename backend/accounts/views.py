from rest_framework import status
from rest_framework.generics import (GenericAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import EmailIsNotConfirmed
from .querysets import ViewsQS
from .serializers import (CustomTokenObtainPairSerializer, DummySerializer,
                          RegisterUserSerializer, UserEmailSerializer,
                          UserSerializer, UserWithRatingSerializer)
from .services import BaseAccountService


class BaseUserMixin:
    """
    Базовый класс для получения профиля пользователя.
    """
    queryset = ViewsQS.list_users()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', ]

    def get_object(self):
        return self.request.user


class BaseUserUpdateProfileMixin(BaseUserMixin):
    """
    Базовый класс для обновления профиля пользователя методом patch.
    """
    http_method_names = ['patch', ]


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

        validated_data: dict = serializer.validated_data
        user = BaseAccountService.create_user(data=validated_data)

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
        user = request.user
        scheme = request.scheme
        domain = request.get_host()

        BaseAccountService.send_email(user=user, scheme=scheme, path='email-confirmation-result', domain=domain,
                                      template_name='email/confirm_email.txt', request_path=request.path)

        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(GenericAPIView):
    """
    Пользователь отправляет GET запрос на url-адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Почтовый адрес успешно подтвержден!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    @BaseAccountService.confirm_with_email
    def get(self, request, user, token_id=None, user_id=None, *args, **kwargs):
        if user:
            BaseAccountService.repository.confirm_email(user)
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)

    def get_serializer_class(self):
        # Возвращает сериализатор-заглушку, так как представление класса не нуждается в сериализаторе
        return DummySerializer


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
        request.session['email'] = email

        # Проверка на то, существует ли такой адрес в БД.
        if BaseAccountService.repository.get_email_exists(email):
            return Response(
                data={"message": self.error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        BaseAccountService.send_email(
            user=request.user, scheme=request.scheme, domain=request.get_host(),
            path='new-email-confirmation-result', template_name='email/confirm_email.txt',
            request_path=request.path
        )

        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmNewEmailAPIView(GenericAPIView):
    """
    Пользователь отправляет GET запрос на адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно поменяли адрес электронной почты!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'
    permission_classes = [IsAuthenticated, ]

    @BaseAccountService.confirm_with_email
    def get(self, request, user, token_id=None, user_id=None, *args, **kwargs):
        if user:
            BaseAccountService.repository.set_new_email(user=user, email=request.session.get('email'))
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)

    def get_serializer_class(self):
        # Возвращает сериализатор-заглушку, так как представление класса не нуждается в сериализаторе
        return DummySerializer


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
        BaseAccountService.repository.make_user_not_active(user=user)
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
        if not BaseAccountService.repository.get_email_exists(email) or user.is_active:
            return Response(data={"message": self.error_message},
                            status=status.HTTP_400_BAD_REQUEST)

        elif user.email == email:
            BaseAccountService.send_email(
                user=user, scheme=request.scheme, domain=request.get_host(),
                path='restore-account-email-confirm',
                template_name='email/restore_account.txt', request_path=request.path
            )

            return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)
        # В случае, если что-то пошло не так
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RestoreAccountFromEmailAPIView(GenericAPIView):
    """
    GET запрос на адрес, полученный в почтовом сообщении - восстановление аккаунта (is_active=True).
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно восстановили свой аккаунт!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    @BaseAccountService.confirm_with_email
    def get(self, request, user, *args, **kwargs):
        if user:
            BaseAccountService.repository.make_user_active(user=user)
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)

    def get_serializer_class(self):
        # Возвращает сериализатор-заглушку, так как представление класса не нуждается в сериализаторе
        return DummySerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    На вход принимает пароль и почтовый адрес пользователя. Возвращает access и refresh_token.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = ViewsQS.list_users()
    http_method_names = ('get',)
    serializer_classes = {
        'retrieve': UserWithRatingSerializer,
        'list': UserSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class UserPersonalProfilePageAPIView(BaseUserMixin, RetrieveAPIView):
    """
    Получение своего профиля.
    """
    serializer_class = UserWithRatingSerializer


class UploadProfileImageAPIView(BaseUserUpdateProfileMixin, UpdateAPIView):
    """
    Обновление картинки профиля пользователя.
    """
    pass


class UploadProfileAboutAPIView(BaseUserUpdateProfileMixin, UpdateAPIView):
    """
    Обновление информации профиля пользователя.
    """
    pass
