import json

from accounts.models import NewUser
from django.urls import reverse
from notifications.models import Notification
from rest_framework.test import APITestCase

from forum.models import Question, QuestionAnswer, ThemeTag


class TestNotificationViewSet(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')

        Notification.objects.create(actor=self.user, recipient=self.user2, verb='Ответил на вопрос',
                                    target=self.question)
        Notification.objects.create(actor=self.user, recipient=self.user2, verb='Ответил на вопрос2',
                                    target=self.question)

        self.url = reverse('notification-list')
        self.detail_url = reverse('notification-detail', kwargs={'pk': 1})

    def test_notification_list(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())

        self.assertIn('type', *content)
        self.assertIn('recipient', *content)
        self.assertIn('actor', *content)
        self.assertIn('verb', *content)
        self.assertIn('target', *content)
        self.assertIn('action_object', *content)

    def test_notification_detail(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.detail_url)
        content = json.loads(response.content.decode())
        print(content)
        self.assertIn('type', content)
        self.assertIn('recipient', content)
        self.assertIn('actor', content)
        self.assertIn('verb', content)
        self.assertIn('target', content)
        self.assertIn('action_object', content)
