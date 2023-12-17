from accounts.models import NewUser
from django.urls import reverse
from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag
from rest_framework import status
from rest_framework.test import APITestCase


class TestCreateCommentAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.comment = AnswerComment.objects.create(user=self.user, comment='Комментарий',
                                                    question_answer=self.answer)

        self.url = reverse('create-comment')

        self.data = {'comment': 'Комментарий 1', 'question_answer': self.answer.id}
        self.data2 = {'comment': '@testuser, Комментарий 2', 'question_answer': self.answer.id,
                      'parent': self.comment.id}

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

        comment = AnswerComment.objects.get(comment='Комментарий 1')
        self.assertIsNotNone(comment)
        self.assertIsNone(comment.user)

    def test_create_comment_referenced_to_parent_comment(self):
        """
        Создаем комментарий, ссылающийся на родительский комментарий по ID.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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


class TestRetrieveComment(APITestCase):

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
        self.url = reverse('detail-comment', kwargs={'pk': self.comment.id})

    def test_retrieve_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCommentParseUser(APITestCase):

    def setUp(self) -> None:

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.comment = AnswerComment.objects.create(user=self.user2, question_answer=self.answer,
                                                    comment='Какой-то комментарий...')

        self.url = reverse('create-comment')

        self.data = {'comment': '@testuser, Комментарий...',
                     'question_answer': self.answer.id, 'parent': self.comment.id}
        self.data2 = {'comment': '@testuser, @testuser3, Комментарий...',
                      'question_answer': self.answer.id, 'parent': self.comment.id}
        self.data3 = {'comment': 'Комментарий..., @testuser',
                      'question_answer': self.answer.id, 'parent': self.comment.id}

    def test_comment_parsed(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.data)

    def test_comment_parsed_two_users_mentioned(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.data2)

    def test_comment_parsed_mention_not_in_the_beginning(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data=self.data3)


class TestCommentParseUserNotifications(APITestCase):

    def setUp(self) -> None:

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq')
        self.user4 = NewUser.objects.create_user(email='testuser4@gmail.com', user_name='testuser4',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')
        self.comment = AnswerComment.objects.create(user=self.user3, question_answer=self.answer,
                                                    comment='Какой-то комментарий...')

        self.url = reverse('create-comment')
        self.data = {'comment': '@testuser2, @testuser3, Комментарий...',
                     'question_answer': self.answer.id, 'parent': self.comment.id}

    def test_comment_parsed_two_users_mentioned(self):
        self.client.force_authenticate(self.user4)
        self.client.post(self.url, data=self.data)
        unread_user2 = self.user2.notifications.unread()
        unread_user3 = self.user3.notifications.unread()
        self.assertEqual(len(unread_user2), 2)    # Уведомления об ответе и упоминании
        self.assertEqual(len(unread_user3), 1)    # Уведомление только об упоминании


class TestCommentNotification(APITestCase):
    """
    Тестируем рассылку уведомлений автору ответа, который
    был прокомментирован другим пользователем.
    """

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')

        self.url = reverse('create-comment')
        self.data = {'comment': 'Комментарий...',
                     'question_answer': self.answer.id}

    def test_user_notified(self):
        self.client.force_authenticate(self.user2)
        self.client.post(self.url, data=self.data)
        unread_user = self.user.notifications.unread()
        self.assertEqual(len(unread_user), 1)
