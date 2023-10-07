import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from favourites.models import Favourite
from forum.models import ThemeTag, Question


class AddToFavourites(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.tag = ThemeTag.objects.create(tag_name='django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.question.tags.add(self.tag)

        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user2)
        self.question.tags.add(self.tag)

        Favourite.objects.create(question=self.question2, user=self.user)

        self.url = reverse('add-to-favourites')

    def test_add_to_favourites_not_authenticated(self):
        response = self.client.post(self.url, data={'question': self.question.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_favourites(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'question': self.question.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_favourites_when_added(self):
        """
        Добавляем в избранное, когда уже там есть. Должно удалиться.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'question': self.question2.pk})
        question2 = self.question2.refresh_from_db()

        self.assertIsNone(question2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestNotificationListView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('favourites')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.tag = ThemeTag.objects.create(tag_name='django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.question.tags.add(self.tag)

        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user2)
        self.question2.tags.add(self.tag)

        self.question3 = Question.objects.create(title='Заголовок3', content='Контент', user=self.user2)
        self.question3.tags.add(self.tag)

        self.question4 = Question.objects.create(title='Заголовок4', content='Контент', user=self.user2)
        self.question4.tags.add(self.tag)

        Favourite.objects.create(user=self.user, question=self.question)
        Favourite.objects.create(user=self.user, question=self.question2)
        Favourite.objects.create(user=self.user, question=self.question3)
        Favourite.objects.create(user=self.user, question=self.question4)

        Favourite.objects.create(user=self.user2, question=self.question)
        Favourite.objects.create(user=self.user2, question=self.question2)

        self.url = reverse('favourites')

    def test_get_list_status_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_content(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), 4)
        self.assertIn('user', content[0])
        self.assertIn('question', content[0])
