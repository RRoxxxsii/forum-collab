from accounts.models import NewUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import (Question, QuestionAnswer, QuestionAnswerImages,
                          ThemeTag)
from forum.tests.test_serializers import generate_photo_file


class TestLeaveAnswerAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('answer-question')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент')
        self.tag = ThemeTag.objects.create(tag_name='django')

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
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')

        self.url = reverse('update-answer', kwargs={'pk': self.answer.id})
        self.data = {'question': self.question.id, 'answer': 'Обновленный ответ...'}

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


class TestQuestionNotification(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)

        self.url = reverse('answer-question')
        self.data = {'question': self.question.id, 'answer': 'Какой-то ответ...'}

    def test_question_owner_get_notified(self):
        """
        Тестируем получение уведомления автором.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.data)
        self.assertEqual(len(self.user2.notifications.unread()), 1)
