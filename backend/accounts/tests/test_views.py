import re

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
        self.url = reverse('confirm-email-request')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq', email_confirmed=True)

    def test_send_request_user_not_authenticated(self):
        """
        Проверка на возвращение статуса 401 для не аутентифицированого пользователя.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_request_user_authenticated(self):
        """
        Проверка отправки письма пользователю и факта получения.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        email_msg = mail.outbox
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(email_msg), 1)

    def test_email_content(self):
        """
        Проверка содержимого отправленого пользователю письма.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url)
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.assertIsNotNone(link)

    def test_email_confirm(self):
        """
        Проверка изменения статуса пользователя email_confirmed.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url)
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_confirmed)

    def test_send_request_email_already_confirmed(self):
        """
        Попытка отправить запрос на получение письма, при этом эл. почта у пользователя
        уже подтверждена.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.post(self.url)
        email_msg = mail.outbox
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(email_msg), 0)
