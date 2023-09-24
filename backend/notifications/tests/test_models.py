from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import AnswerComment, Question, QuestionAnswer, ThemeTag
from notifications.models import Notification
from notifications.utils import notify


class TestCreateNotification(APITestCase):

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

    def test_create_notification_for_question(self):
        """
        Создаем уведомление для пользователя, который является автором вопроса.
        Уведомление - пользователь получил ответ на вопрос.
        Уведомление получает автор вопроса.
        """
        notify(receiver=self.user,
               sender=self.user2,
               target=self.question,
               action_obj=self.answer)
        notification = Notification.objects.all().first()

        self.assertEqual(notification.action_obj_content_type.model, 'questionanswer')
        self.assertEqual(notification.action_obj_object_id, self.answer.id)
        self.assertEqual(notification.target_content_type.model, 'question')
        self.assertEqual(notification.target_object_id, self.question.id)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.receiver, self.user)

    def test_create_notification_for_question_without_action_object(self):
        """
        Создаем уведомление для пользователя, который является автором вопроса.
        Не указываем action_obj.
        """
        notify(receiver=self.user,
               sender=self.user2,
               target=self.question)
        notification = Notification.objects.all().first()

        self.assertEqual(notification.action_obj_content_type, None)
        self.assertEqual(notification.target_content_type.model, 'question')
        self.assertEqual(notification.target_object_id, self.question.id)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.receiver, self.user)

    def test_create_notification_for_answer(self):
        """
        Создаем уведомление для пользователя, который является автором ответа.
        Уведомление получает автор ответа.
        """
        notify(receiver=self.user2,
               sender=self.user3,
               target=self.answer,
               action_obj=self.comment)
        notification = Notification.objects.all().first()

        self.assertEqual(notification.action_obj_content_type.model, 'answercomment')
        self.assertEqual(notification.action_obj_object_id, self.comment.id)
        self.assertEqual(notification.target_content_type.model, 'questionanswer')
        self.assertEqual(notification.target_object_id, self.answer.id)
        self.assertEqual(notification.sender, self.user3)
        self.assertEqual(notification.receiver, self.user2)

    def test_create_notification_for_answer_without_action_obj(self):
        """
        Создаем уведомление для пользователя, который является автором ответа.
        Не указываем action_obj.
        """
        notify(receiver=self.user2,
               sender=self.user3,
               target=self.answer)
        notification = Notification.objects.all().first()

        self.assertEqual(notification.action_obj_content_type, None)
        self.assertEqual(notification.target_content_type.model, 'questionanswer')
        self.assertEqual(notification.target_object_id, self.answer.id)
        self.assertEqual(notification.sender, self.user3)
        self.assertEqual(notification.receiver, self.user2)

    def test_notification_answer_rated(self):
        """
        Тестируем шаблон уведомлений после того, как ответ был отмечен решающим.
        """
        notify(receiver=self.user2,
               sender=self.user,
               text='ответ был отмечен решенным',
               target=self.answer)
        notification = Notification.objects.all().first()
        self.assertEqual(notification.action_obj_content_type, None)
        self.assertEqual(notification.target_content_type.model, 'questionanswer')
        self.assertEqual(notification.target_object_id, self.answer.id)
        self.assertEqual(notification.text, 'ответ был отмечен решенным')

    def test_notification_author_is_receiver(self):
        """
        Если отправитель является получателем, то уведомление не создаем.
        """
        notify(receiver=self.user2,
               sender=self.user2,
               target=self.answer)

        self.assertEqual(len(Notification.objects.all()), 0)


class TestNotificationQuerySet(APITestCase):

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

    def test_mark_all_as_read(self):
        notifications_unread = Notification.objects.filter(unread=True)
        self.assertEqual(len(notifications_unread), len(Notification.objects.all()))

        # Проверяем, прочитаны ли получателем его уведомлений
        notifications_unread.mark_all_as_read(receiver=self.user)
        notifications_read = Notification.objects.filter(unread=False)
        self.assertEqual(len(notifications_read), len(Notification.objects.all()))
        self.assertEqual(
            len(self.user.receiver_notifications.filter(unread=False)),
            len(Notification.objects.all())
        )

    def test_mark_all_as_unread(self):
        notifications_unread = Notification.objects.filter(unread=True)
        notifications_unread.update(unread=False)
        notifications_read = Notification.objects.filter(unread=False)
        self.assertEqual(len(notifications_read), len(Notification.objects.all()))

        notifications_read.mark_all_as_unread(receiver=self.user)
        self.assertEqual(len(notifications_read), len(Notification.objects.filter(unread=True)))
        self.assertEqual(
            len(self.user.receiver_notifications.filter(unread=True)),
            len(Notification.objects.all())
        )
