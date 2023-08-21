import json

from django.db.models import QuerySet
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, ThemeTag
from forum.serializers import TagFieldSerializer


class TestUserAskQuestionPost(APITestCase):
    """
    Тестирует AskQuestionAPIView; создание вопроса. Отправка post-запроса.
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

        self.ask_data = {"title": "Заголовок1", "content": "Вопрос. Не знаю как решить пробелему..",
                         "tags": ['django']}
        self.ask_data2 = {'title': 'Заголовок2', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tags': ['django', 'react']}
        self.ask_data3 = {'title': 'Заголовок3', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tags': ['django', 'react', 'python', 'nextjs', 'C#',
                                   'django-rest-framework']}
        self.ask_data4 = {"title": "Заголовок4", "content": "Вопрос. Не знаю как решить пробелему..",
                          "tags": ['dj']}
        self.ask_data5 = {"title": "Заголовок5", "content": "Вопрос. Не знаю как решить пробелему..",
                          "tags": ['django', 'r', 'react']}
        self.ask_data6 = {"title": "Заголовок6", "content": "Вопрос. Не знаю как решить пробелему..",
                          "tags": []}
        self.ask_data7 = {"title": "Заголовок7", "content": "Вопрос. Не знаю как решить пробелему.."}

    def test_user_not_authenticated(self):
        response = self.client.post(self.url, data=self.ask_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_with_one_tag(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data)
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

    def test_send_request_with_tag_does_not_exist_status_code(self):
        """
        Отправка запроса с одним тегом, которого не сущетсвует.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_request_with_tag_does_not_exist_content(self):
        """
        Отправка запроса с одним тегом, которого не сущетсвует.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.ask_data4)
        new_tag = ThemeTag.objects.get(tag='dj')

        self.assertEqual(new_tag.tag, 'dj')
        self.assertEqual(new_tag.user, self.user)

        self.assertFalse(new_tag.is_relevant)
        self.assertTrue(new_tag.is_user_tag)

    def test_send_request_with_tags_dont_exist_status_code(self):
        """
        Отправка запроса с тегами, среди которых есть существующие и несуществующие.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data5)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_request_with_tags_dont_exist_content(self):
        """
        Отправка запроса с тегами, среди которых есть существующие и несуществующие.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.ask_data5)
        new_tag = ThemeTag.objects.get(tag='r')

        self.assertEqual(new_tag.tag, 'r')
        self.assertEqual(new_tag.user, self.user)

        self.assertFalse(new_tag.is_relevant)
        self.assertTrue(new_tag.is_user_tag)

    def test_question_data(self):
        """
        Проверка, действительно ли теги сохраняются к вопросу.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.ask_data5)
        question = Question.objects.get(title='Заголовок5')
        tags = question.tags.all()
        self.assertEqual(len(tags), 3)

    def test_send_request_without_empty_tags(self):
        """
        Отправка запросов с пустым списком тегов.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data6)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_request_without_tags(self):
        """
        Отправка запросов без тегов.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data7)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserAskQuestionGet(APITestCase):
    """
    Тестирует AskQuestionAPIView; работа с тегами через query_params.
    """
    def setUp(self) -> None:
        self.url = '/api/v1/forum/ask-question/'

        self.tag1 = ThemeTag.objects.create(tag='django')
        self.tag2 = ThemeTag.objects.create(tag='react')
        self.tag3 = ThemeTag.objects.create(tag='python')
        self.tag4 = ThemeTag.objects.create(tag='nextjs')
        self.tag5 = ThemeTag.objects.create(tag='C#')
        self.tag6 = ThemeTag.objects.create(tag='Java')
        self.tag7 = ThemeTag.objects.create(tag='django-rest-framework')

        self.question1 = Question.objects.create(title='Заголовок', content='Контент')
        self.question1.tags.add(self.tag1.id, self.tag7.id)

        self.question2 = Question.objects.create(title='Заголовок', content='Контент')
        self.question2.tags.add(self.tag1.id)

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

    def test_get_request_without_query_params(self):
        """
        Отправка GET запроса, без указания query_params.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_with_query_params_status_code(self):
        """
        Тестирование статус-кода ответа. Ожидается 200.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(f'{self.url}?q=dj')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_query_params_content(self):
        """
        Тестирование содержимого ответа.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(f'{self.url}?q=dj')
        content = json.loads(response.content.decode())
        first_dict, second_dict = content[0], content[1]

        self.assertEqual(first_dict.get('tag'), 'django')
        self.assertEqual(first_dict.get('use_count'), 2)
        self.assertEqual(second_dict.get('tag'), 'django-rest-framework')
        self.assertEqual(second_dict.get('use_count'), 1)

    def test_request_with_tag_does_not_exist(self):
        """
        Совпадений с тегом не найдено. Ожидается исключение 400.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(f'{self.url}?q=no-similarities')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestThemeTagMakingTagRelevantAskQuestion(APITestCase):
    """
    Тестирует изменение статуса тега на релевантный при создании вопроса.
    """

    def setUp(self) -> None:
        self.url = '/api/v1/forum/ask-question/'

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.tag1 = ThemeTag.objects.create(tag='django', is_user_tag=True, is_relevant=False)
        self.tag2 = ThemeTag.objects.create(tag='django-rest-framework', is_relevant=False)

    def test_tag_is_relevant(self):

        for i in range(9):
            self.client.force_authenticate(self.user)
            title, content = f'title{i}', f'content{i}'
            self.client.post(self.url, {'title': title, 'content': content, 'tags': [self.tag1]})

        self.tag1.refresh_from_db()
        self.assertFalse(self.tag1.is_relevant)

        # 10-ый вопрос, когда is_relevant становится True

        self.client.post(self.url, {'title': 'title10', 'content': 'content10', 'tags': [self.tag1]})

        self.tag1.refresh_from_db()
        self.assertTrue(self.tag1.is_relevant)

    def test_tag_relevant_but_not_user_tag(self):
        """
        Тег не является пользовательским и при количестве запросов больше 10
        не должен автоматически становиться is_relevant=True
        """
        for i in range(9):
            self.client.force_authenticate(self.user)
            title, content = f'title{i}', f'content{i}'
            self.client.post(self.url, {'title': title, 'content': content, 'tags': [self.tag2]})

        self.tag1.refresh_from_db()
        self.assertFalse(self.tag1.is_relevant)

        # 10-ый вопрос, когда is_relevant становится True

        self.client.post(self.url, {'title': 'title10', 'content': 'content10', 'tags': [self.tag2]})

        self.tag1.refresh_from_db()
        self.assertFalse(self.tag1.is_relevant)
