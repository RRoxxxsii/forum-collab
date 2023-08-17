from django.db.models import QuerySet
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, ThemeTag
from forum.serializers import TagFieldSerializer


class TestUserAskQuestionPost(APITestCase):
    """
    Тестирует AskQuestionAPIView; создание вопроса.
    """
    def setUp(self) -> None:
        self.url = reverse('ask-question')

        tag1 = ThemeTag.objects.create(tag='django')
        tag2 = ThemeTag.objects.create(tag='react')
        tag3 = ThemeTag.objects.create(tag='python')
        tag4 = ThemeTag.objects.create(tag='nextjs')
        tag5 = ThemeTag.objects.create(tag='C#')
        tag6 = ThemeTag.objects.create(tag='Java')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.ask_data = {"title": "Заголовок", "content": "Вопрос. Не знаю как решить пробелему..",
                         "tag_ids": [tag1.id]}
        self.ask_data2 = {'title': 'Заголовок', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tag_ids': [tag1.id, tag2.id]}
        self.ask_data3 = {'title': 'Заголовок', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tag_ids': [tag1.id, tag2.id, tag3.id, tag4.id, tag5.id, tag6.id]}

    def test_user_not_authenticated(self):
        response = self.client.post(self.url, data=self.ask_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_with_one_tag(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_with_several_tags(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data2)
        question = Question.objects.all()[0]
        queryset = question.tags.all()

        self.assertEqual(len(queryset), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_request_with_more_than_five_tags(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserAskQuestionGet(APITestCase):
    """
    Тестирует AskQuestionAPIView; работа с тегами через query_params.
    """
    def setUp(self) -> None:
        self.url = reverse('ask-question')

        self.tag1 = ThemeTag.objects.create(tag='django')
        self.tag2 = ThemeTag.objects.create(tag='react')
        self.tag3 = ThemeTag.objects.create(tag='python')
        self.tag4 = ThemeTag.objects.create(tag='nextjs')
        self.tag5 = ThemeTag.objects.create(tag='C#')
        self.tag6 = ThemeTag.objects.create(tag='Java')
        self.tag7 = ThemeTag.objects.create(tag='django-rest-framework')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.ask_data = {"title": "Заголовок", "content": "Вопрос. Не знаю как решить пробелему..",
                         "tag_ids": [self.tag1.id]}
        self.ask_data2 = {'title': 'Заголовок', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'theme_tags': [self.tag1, self.tag2]}
        self.ask_data3 = {'title': 'Заголовок', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'theme_tags': [self.tag1, self.tag2, self.tag3, self.tag4, self.tag5, self.tag6]}

    def test_get_request_without_query_params(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_query_params(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data={'q': 'dja'})
        self.assertEqual(response.content.decode(), TagFieldSerializer(data=['django', 'django_rest_framework']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


