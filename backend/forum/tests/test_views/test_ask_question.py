import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, QuestionImages, ThemeTag
from forum.tests.test_serializers import generate_photo_file


class TestUserAskQuestionPost(APITestCase):
    """
    Тестирует AskQuestionAPIView; создание вопроса. Отправка post-запроса.
    """
    def setUp(self) -> None:
        self.url = reverse('ask-question')

        ThemeTag.objects.create(tag_name='django')
        ThemeTag.objects.create(tag_name='react')
        ThemeTag.objects.create(tag_name='python')
        ThemeTag.objects.create(tag_name='nextjs')
        ThemeTag.objects.create(tag_name='C#')
        ThemeTag.objects.create(tag_name='Java')

        photo = generate_photo_file()
        photo2 = generate_photo_file()
        photo3 = generate_photo_file()
        photo4 = generate_photo_file()

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

        self.ask_data8 = {'title': 'Заголовок3', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tags': ['django', 'react', 'python', 'nextjs', 'C#'],
                          'uploaded_images': [photo]}

        self.ask_data9 = {'title': 'Заголовок3', 'content': 'Вопрос. Не знаю как решить пробелему..',
                          'tags': ['django', 'react', 'python', 'nextjs', 'C#'],
                          'uploaded_images': [photo, photo2]}
        self.ask_data10 = {'title': 'Заголовок3', 'content': 'Вопрос. Не знаю как решить пробелему..',
                           'tags': ['django', 'react', 'python', 'nextjs', 'C#'],
                           'uploaded_images': [photo, photo2, photo3, photo4]}
        self.ask_data11 = {'title': 'Заголовок', 'tags': ['django', 'react', 'python', 'nextjs', 'C#']}

    def test_user_not_authenticated(self):
        response = self.client.post(self.url, data=self.ask_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_question_without_content(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data11)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        new_tag = ThemeTag.objects.get(tag_name='dj')

        self.assertEqual(new_tag.tag_name, 'dj')
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
        new_tag = ThemeTag.objects.get(tag_name='r')

        self.assertEqual(new_tag.tag_name, 'r')
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

    def test_ask_question_with_image_status_code(self):
        """
        Код ответа с одной отправленной фотографией.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data8)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ask_question_with_two_images_status_code(self):
        """
        Код ответа с одной отправленной фотографией.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data9)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ask_question_with_image_content_created(self):
        """
        Существует ли фотография в БД.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.ask_data8)

        self.assertEqual(len(QuestionImages.objects.all()), 1)

    def test_ask_question_with_two_images_content_create(self):
        """
        Существует ли несколько переданных фотографий в БД.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.ask_data9)
        self.assertEqual(len(QuestionImages.objects.all()), 2)

    def test_ask_question_with_more_than_three_images(self):
        """
        Отправляем запрос с числом вложений больше 3.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.ask_data10)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserAskQuestionGet(APITestCase):
    """
    Тестирует AskQuestionAPIView; работа с тегами через query_params.
    """
    def setUp(self) -> None:
        self.url = reverse('ask-question')

        self.tag1 = ThemeTag.objects.create(tag_name='django')
        self.tag2 = ThemeTag.objects.create(tag_name='react')
        self.tag3 = ThemeTag.objects.create(tag_name='python')
        self.tag4 = ThemeTag.objects.create(tag_name='nextjs')
        self.tag5 = ThemeTag.objects.create(tag_name='C#')
        self.tag6 = ThemeTag.objects.create(tag_name='Java')
        self.tag7 = ThemeTag.objects.create(tag_name='django-rest-framework')

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

        self.assertEqual(first_dict.get('tag_name'), 'django')
        self.assertEqual(first_dict.get('use_count'), 2)
        self.assertEqual(second_dict.get('tag_name'), 'django-rest-framework')
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
        self.url = reverse('ask-question')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.tag1 = ThemeTag.objects.create(tag_name='django', is_user_tag=True, is_relevant=False)
        self.tag2 = ThemeTag.objects.create(tag_name='django-rest-framework', is_relevant=False)

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

