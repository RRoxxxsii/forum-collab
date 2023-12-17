import json

from accounts.models import NewUser
from django.urls import reverse
from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag
from notifications.models import Notification
from rest_framework.test import APITestCase


class TestNotifications(APITestCase):

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
        self.notification1 = Notification.objects.create(receiver=self.user, sender=self.user2,
                                                         target=self.question, action_obj=self.answer)
        self.notification2 = Notification.objects.create(receiver=self.user, sender=self.user2,
                                                         target=self.question, action_obj=self.answer)
        self.notification3 = Notification.objects.create(receiver=self.user, sender=self.user2,
                                                         target=self.question, action_obj=self.answer)
        self.notification4 = Notification.objects.create(receiver=self.user, sender=self.user2,
                                                         target=self.question, action_obj=self.answer)
        self.notification5 = Notification.objects.create(receiver=self.user, sender=self.user2,
                                                         target=self.question, action_obj=self.answer)

        self.url = reverse('notifications')
        self.url_to_update = reverse('mark-as-read')

    def test_notifications_list_content(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        notification_1 = content[0]

        self.assertIn('level', notification_1)
        self.assertIn('target_object_id', notification_1)
        self.assertIn('action_obj_object_id', notification_1)
        self.assertIn('sender', notification_1)
        self.assertIn('receiver', notification_1)
        self.assertIn('target_content_type', notification_1)
        self.assertIn('action_obj_content_type', notification_1)

    def test_mark_all_as_read(self):
        self.client.force_authenticate(self.user)
        self.client.patch(self.url_to_update,
                          data={'list_id': [int(self.notification1.id), int(self.notification2.id)]})
        self.assertEqual(len(self.user.notifications.unread()), 3)
        self.assertEqual(len(self.user.notifications.read()), 2)
        self.assertEqual(len(self.user.notifications.all()), 5)
