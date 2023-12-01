from rest_framework import status
from rest_framework.generics import (GenericAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .dto import (ConfirmByEmailDTO, ConfirmByEmailWithEmailDTO, CreateUserDTO,
                  RequestForConfirmationEmailDTO)
from .permissions import EmailIsNotConfirmed
from .querysets import UsersQS
from .repository import BaseAccountRepository
from .serializers import (CustomTokenObtainPairSerializer,
                          RegisterUserSerializer, UserEmailSerializer,
                          UserSerializer, UserWithRatingSerializer)
from .services import (CreateUserService, PerformActionWhenConfirm,
                       SendConfirmationEmailService)


class BaseUserMixin:
    """
    Базовый класс для получения профиля пользователя.
    """
    queryset = UsersQS.get_obj_list()
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


class CustomUserRegisterAPIView(APIView):
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
        user = CreateUserService().execute(data=CreateUserDTO(**validated_data))

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

    def get(self, request):
        user = request.user
        dto = RequestForConfirmationEmailDTO(
            user=user, path='email-confirmation-result',
            template_name='email/confirm_email.txt', request_path=request.build_absolute_uri()

        )
        SendConfirmationEmailService().execute(data=dto)
        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос на url-адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Почтовый адрес успешно подтвержден!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        dto = ConfirmByEmailDTO(
            user_id=query_params.get('user_id'), token_id=query_params.get('token_id'), user=request.user
        )
        is_success = PerformActionWhenConfirm().confirm_email(dto)
        if is_success:
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)


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
        if BaseAccountRepository.get_email_exists(email):
            return Response(
                data={"message": self.error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        dto = RequestForConfirmationEmailDTO(
            user=request.user, path='new-email-confirmation-result',
            template_name='email/confirm_email.txt', request_path=request.build_absolute_uri()
        )
        SendConfirmationEmailService().execute(data=dto)

        return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)


class ConfirmNewEmailAPIView(APIView):
    """
    Пользователь отправляет GET запрос на адрес, полученный в почтовом сообщении и email_confirmed=True.
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно поменяли адрес электронной почты!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        dto = ConfirmByEmailWithEmailDTO(
            user=request.user,
            token_id=query_params.get('token_id'),
            user_id=query_params.get('user_id'),
            email=request.session.get('email')
        )
        is_success = PerformActionWhenConfirm().set_new_email(dto)
        if is_success:
            del request.session['email']
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)


class DeleteAccountAPIView(GenericAPIView):
    """
    GET-запрос - аккаунт пользователя удаляется(is_active=False), но остается в БД.
    При успешном выполнении возвращается код статуса 200 и success_message.
    """
    permission_classes = [IsAuthenticated, ]
    success_message = 'Аккаунт удален. Вы можете восстановить его в течение 6 месяцев '

    def get(self, request):
        user = request.user
        BaseAccountRepository.make_user_not_active(user=user)
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
        if not BaseAccountRepository.get_email_exists(email) or user.is_active:
            return Response(data={"message": self.error_message},
                            status=status.HTTP_400_BAD_REQUEST)

        elif user.email == email:
            dto = RequestForConfirmationEmailDTO(
                user=user, path='restore-account-email-confirm',
                template_name='email/restore_account.txt', request_path=request.build_absolute_uri()
            )

            SendConfirmationEmailService().execute(data=dto)

            return Response(data={"message": self.success_message}, status=status.HTTP_201_CREATED)
        # В случае, если что-то пошло не так
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RestoreAccountFromEmailAPIView(APIView):
    """
    GET запрос на адрес, полученный в почтовом сообщении - восстановление аккаунта (is_active=True).
    При успешном запросе: status 200 и success message; В противном случае: status 400 и error message.
    """
    success_message = 'Вы успешно восстановили свой аккаунт!'
    error_message = 'К сожалению, что-то пошло не так. Пожалуйста, попробуйте снова.'

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        token_id = query_params.get('token_id')
        user_id = query_params.get('user_id')
        user = request.user

        dto = ConfirmByEmailDTO(token_id=token_id, user_id=user_id, user=user)
        is_success = PerformActionWhenConfirm().make_user_active(dto)
        if is_success:
            return Response(data=self.success_message, status=200)
        return Response(data=self.error_message, status=400)


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    На вход принимает пароль и почтовый адрес пользователя. Возвращает access и refresh_token.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = UsersQS.get_obj_list()
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
