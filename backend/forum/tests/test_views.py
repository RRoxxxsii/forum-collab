import io
import json
import random

from accounts.models import NewUser
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionAnswerRating,
                          QuestionImages, QuestionRating, ThemeTag)


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = f'test{random.randint(1, 1000000)}.png'
    file.seek(0)
    return file


class TestUserAskQuestionPost(APITestCase):
    """
    Тестирует AskQuestionAPIView; создание вопроса. Отправка post-запроса.
    """
    def setUp(self) -> None:
        self.url = reverse('ask-question')

        ThemeTag.objects.create(tag='django')
        ThemeTag.objects.create(tag='react')
        ThemeTag.objects.create(tag='python')
        ThemeTag.objects.create(tag='nextjs')
        ThemeTag.objects.create(tag='C#')
        ThemeTag.objects.create(tag='Java')

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


class TestUpdateDestroyQuestionAPIView(APITestCase):
    """
    Обновление вопроса.
    """
    def setUp(self) -> None:
        self.tag1 = ThemeTag.objects.create(tag='django')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question1 = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.question1.tags.add(self.tag1.id)

        self.url = reverse('update-question', kwargs={'pk': self.question1.id})
        self.data = {'content': 'Обновленный вопрос'}

    def test_update_question_not_owner(self):
        """
        Обновление вопроса не являясь автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_question_not_authenticated(self):
        """
        Пользователь не аутентифицирован.
        """
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_question(self):
        """
        Обновление ответа с помощью метода put.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_question_not_owner(self):
        """
        Get-запрос на вопрос, не являясь автором. Ожидается открытый доступ.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_authenticated(self):
        """
        Get-запрос, не аутентифицированный.
        """
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question_not_owner(self):
        """
        Удаление вопроса, не являясь его автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question(self):
        """
        Удаление вопроса автором.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestThemeTagMakingTagRelevantAskQuestion(APITestCase):
    """
    Тестирует изменение статуса тега на релевантный при создании вопроса.
    """

    def setUp(self) -> None:
        self.url = reverse('ask-question')

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


class TestLeaveAnswerAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('answer-question')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент')
        self.tag = ThemeTag.objects.create(tag='django')

        photo = generate_photo_file()
        photo2 = generate_photo_file()

        self.question.tags.add(self.tag)
        self.answer_data = {'answer': 'Ответ...', 'question': self.question.id}
        self.answer_data2 = {'answer': 'Ответ...', 'question': self.question.id,
                             'uploaded_images': [photo]}
        self.answer_data3 = {'answer': 'Ответ...', 'question': self.question.id,
                             'uploaded_images': [photo, photo2]}

    def test_answer_question_user_not_authenticated_status_code(self):
        """
        Пользователь не аутентифицирован.
        """
        response = self.client.post(self.url, data=self.answer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_question_user_not_authenticated_content_created(self):
        """
        Пользователь не аутентифицирован. Проверка сохранения в БД.
        """
        self.client.post(self.url, data=self.answer_data)
        answer = QuestionAnswer.objects.first()
        self.assertIsNotNone(answer)
        self.assertIsNone(answer.user)

    def test_answer_question(self):
        """
        Пользователь аутентифицирован.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.answer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_with_one_question_status_code(self):
        """
        Создание ответа с одним вложением. Проверка кода ответа.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.answer_data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_with_one_question_content_created(self):
        """
        Создание ответа с одним вложением. Проверка сохранения вложений в БД.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.answer_data2)
        self.assertEqual(len(QuestionAnswerImages.objects.all()), 1)

    def test_answer_with_several_question_status_code(self):
        """
        Создание ответа с более чем одним вложением.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.answer_data3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateDestroyAnswerAPIView(APITestCase):
    """
    Обновление ответа.
    """
    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.tag = ThemeTag.objects.create(tag='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')

        self.url = reverse('update-answer', kwargs={'pk': self.answer.id})
        self.data = {'question': self.question, 'answer': 'Обновленный ответ...'}

    def test_update_answer_not_owner(self):
        """
        Обновление ответа не являясь автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_answer_not_authenticated(self):
        """
        Пользователь не аутентифицирован.
        """
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_answer(self):
        """
        Обновление ответа с помощью метода put.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answer_not_owner(self):
        """
        Get-запрос на ответ, не являясь автором. Ожидается открытый доступ.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_authenticated(self):
        """
        Get-запрос, не аутентифицированный.
        """
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer_not_owner(self):
        """
        Удаление ответа, не являясь его автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_answer(self):
        """
        Удаление ответа автором.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCreateCommentAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')

        self.url = reverse('create-comment')

        self.data = {'comment': 'Комментарий...', 'question_answer': self.answer.id}

    def test_comment_user_not_authenticated_status_code(self):
        """
        Пользователь не аутентифицирован. Код ответа.
        """
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_user_not_authenticated_content_created(self):
        """
        Пользователь не аутентифицирован. Проверка сохранения в БД.
        """
        self.client.post(self.url, data=self.data)

        comment = AnswerComment.objects.first()
        self.assertIsNotNone(comment)
        self.assertIsNone(comment.user)

    def test_comment_status_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestUpdateCommentAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.comment = AnswerComment.objects.create(comment='Комментарий..', user=self.user,
                                                    question_answer=self.answer)
        self.url = reverse('update-comment', kwargs={'pk': self.comment.id})
        self.data = {'comment': 'Обновленный комментарий...'}

    def test_update_comment_not_owner(self):
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestLikeDislikeAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.tag = ThemeTag.objects.create(tag='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')

    def test_user_not_authenticated(self):
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_author(self):
        """
        Пользователь оценивает свою запись. Действие должно быть недоступно.
        """
        self.client.force_authenticate(self.user2)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_question_status_code(self):
        """
        Тестируем код ответа при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_question_created_question(self):
        """
        Тестируем создание лайка при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_question_status_code(self):
        """
        Тестируем код ответа при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_question_created(self):
        """
        Тестируем создание дизлайка при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 0)
        self.assertEqual(rating.dislike_amount, 1)

    def test_like_answer_status_code(self):
        """
        Тестируем код ответа при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.answer.pk})
        response = self.client.get(f'{url}?model=answer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_answer_created(self):
        """
        Тестируем создание лайка при отправке запроса к овтету.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')
        rating = QuestionAnswerRating.objects.first()
        self.assertEqual(rating.like_amount, 1)
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_answer_status_code(self):
        """
        Тестируем код ответа при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.answer.pk})
        response = self.client.get(f'{url}?model=answer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_answer_created(self):
        """
        Тестируем создание дизлайка при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')
        rating = QuestionAnswerRating.objects.first()
        self.assertEqual(rating.like_amount, 0)
        self.assertEqual(rating.dislike_amount, 1)

    def test_unlike(self):
        """
        Убираем лайк.
        """
        # Сначала ставим лайк
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)

        # Повторно отправляем запрос на этот же url, тем самым удаляя лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 0)

    def test_like_when_disliked(self):
        """
        Пользователь лайкает, когда уже стоит дизлайк.
        """
        # Создаем дизлайк для пользователя
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Cтавим лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 0)

        # Проверяем, поставился ли лайк
        self.assertEqual(rating.like_amount, 1)

    def test_undislike(self):
        """
        Убираем дизлайк.
        """
        self.client.force_authenticate(self.user)
        # Cоздаем дизлайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 1)

        # Повторно отправляем запрос на этот же url, тем самым удаляя лайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_when_liked(self):
        """
        Пользователь ставит дизлайк, когда уже стоит лайк.
        """
        self.client.force_authenticate(self.user)
        # Ставим лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)

        # Ставим дизлайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 1)
