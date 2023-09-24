import json

from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, ThemeTag, QuestionAnswer, AnswerComment
from notifications.models import Notification


class TestNotificationsListAPIView(APITestCase):

    def setUp(self) -> None:

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок вопроса', content='Контент вопроса',
                                                user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')
        self.comment = AnswerComment.objects.create(user=self.user3, question_answer=self.answer,
                                                    comment='Какой-то комментарий...')
        for i in range(5):
            Notification.objects.create(receiver=self.user,
                                        sender=self.user2,
                                        target=self.question,
                                        action_obj=self.answer)

        self.url = reverse('notifications')

    def test_notifications_list_content(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        notification_1 = content[0]

        self.assertIn('level', content)
        self.assertIn('target_object_id', content)
        self.assertIn('action_object_id', content)
        self.assertIn('sender', content)
        self.assertIn('receiver', content)
        self.assertIn('target_content_type', content)
        self.assertIn('action_obj_content_type', content)
