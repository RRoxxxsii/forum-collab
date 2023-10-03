from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import ThemeTag, Question


class AddToFavourites(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)

        self.url = reverse('add-to-favourites')

    def test_add_to_favourites_not_authenticated(self):
        response = self.client.post(self.url, data={'question': self.question.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_favourites(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'question': self.question.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestNotificationListView(APITestCase):

    def setUp(self) -> None:
        pass
