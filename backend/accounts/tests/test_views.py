from accounts.models import NewUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegistrationAPI(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('create-account')

    def test_register_user(self):
        """
        Testing user registrations.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': 'Ax6!a7OpNvq'})
        new_user = NewUser.objects.get(email='a@a.ru')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(new_user)

    def test_register_user_simple_password(self):
        """
        Password is too simple, supposed to raise exception.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': '12345'})
        self.assertEqual(response.status_code, 400)

