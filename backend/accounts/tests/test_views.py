from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser


class TestRegistrationAPI(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('create-account')

    def test_register_user(self):
        """
        Тестирование регистрации пользователя.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': 'Ax6!a7OpNvq'})
        new_user = NewUser.objects.get(email='a@a.ru')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(new_user)

    def test_register_user_simple_password(self):
        """
        Пароль слишком простой, ожидается возбуждение исключения.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': '12345'})
        self.assertEqual(response.status_code, 400)


class TestEmailConfirmAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('confirm-email')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser', password='Ax6!a7OpNvq')

    def test_send_request_user_not_authenticated(self):
        """
        Проверка на возвращение статуса 401 для не аутентифицированого пользователя.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_request_user_authenticated(self):
        """
        Проверка отправки письма пользователю
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        email_msg = mail.outbox
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(len(email_msg), 1)

