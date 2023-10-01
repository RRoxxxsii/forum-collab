from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import ThemeTag, Question


class TestNewUserModelTest(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', email_confirmed=True, is_active=True)
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq', email_confirmed=True, is_active=True)
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq', email_confirmed=True, is_active=True)
        self.user4 = NewUser.objects.create_user(email='testuser4@gmail.com', user_name='testuser4',
                                                 password='Ax6!a7OpNvq', email_confirmed=True, is_active=True)

        self.tag = ThemeTag.objects.create(tag_name=f'django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user, is_solved=True)
        self.question.tags.add(self.tag)

        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user2, is_solved=True)
        self.question2.tags.add(self.tag)

        self.question.like(user=self.user2)
        self.question.like(user=self.user3)
        self.question.like(user=self.user4)

        self.question2.like(user=self.user)
        self.question2.like(user=self.user3)
        self.question2.like(user=self.user4)

    def test_count_question_user_likes(self):

        self.assertEqual(self.user.count_question_likes(), self.question.rating.like_amount)
        self.assertEqual(self.user2.count_question_likes(), self.question2.rating.like_amount)
