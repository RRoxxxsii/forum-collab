from accounts.models import NewUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag


class TestCreateCommentAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
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
        """
        Пользователь аутентифицирован.
        """
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
        self.tag = ThemeTag.objects.create(tag_name='django')
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

