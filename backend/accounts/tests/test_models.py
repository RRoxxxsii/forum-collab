from django.core.cache import cache
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, QuestionAnswer, ThemeTag


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
        self.user5 = NewUser.objects.create_user(email='testuser5@gmail.com', user_name='testuser5',
                                                 password='Ax6!a7OpNvq', is_active=True)

        self.tag = ThemeTag.objects.create(tag_name=f'django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user, is_solved=True)
        self.question.tags.add(self.tag)

        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user2)
        self.question2.tags.add(self.tag)

        self.answer = QuestionAnswer.objects.create(question=self.question2, user=self.user, answer='Ответ',
                                                    is_solving=True)
        self.answer2 = QuestionAnswer.objects.create(question=self.question2, user=self.user2, answer='Ответ')

        self.question.like(user=self.user2)
        self.question.like(user=self.user3)
        self.question.like(user=self.user4)
        self.question.dislike(user=self.user5)

        self.question2.like(user=self.user)
        self.question2.like(user=self.user3)
        self.question2.like(user=self.user4)
        self.question2.dislike(user=self.user5)

        self.answer.like(user=self.user2)
        self.answer.like(user=self.user3)
        self.answer.like(user=self.user4)
        self.answer.dislike(user=self.user5)

        self.answer2.like(user=self.user)
        self.answer2.like(user=self.user3)
        self.answer2.like(user=self.user4)
        self.answer2.dislike(user=self.user5)

    def test_count_question_user_likes(self):
        self.assertEqual(self.user.count_question_likes(), self.question.rating.like_amount)
        self.assertEqual(self.user2.count_question_likes(), self.question2.rating.like_amount)

    def test_count_question_user_dislikes(self):
        self.assertEqual(self.user.count_question_dislikes(), self.question.rating.dislike_amount)
        self.assertEqual(self.user2.count_question_dislikes(), self.question2.rating.dislike_amount)

    def test_count_answer_user_likes(self):
        self.assertEqual(self.user.count_answer_likes(), self.answer.rating.like_amount)
        self.assertEqual(self.user2.count_answer_likes(), self.answer2.rating.like_amount)

    def test_count_answer_user_dislikes(self):
        self.assertEqual(self.user.count_answer_dislikes(), self.answer.rating.dislike_amount)
        self.assertEqual(self.user2.count_answer_dislikes(), self.answer2.rating.dislike_amount)

    def test_get_amount_questions_solved(self):
        self.assertEqual(self.user.get_amount_question_solved(), 1)
        self.assertEqual(self.user2.get_amount_question_solved(), 0)

    def test_count_karma(self):
        user_karma = self.user.count_karma()
        user2_karma = self.user2.count_karma()

        self.assertEqual(user_karma, 26)
        self.assertEqual(user2_karma, 16)

    def test_count_likes_return_when_no_likes(self):
        self.assertEqual(self.user5.count_question_likes(), 0)
        self.assertEqual(self.user5.count_answer_likes(), 0)

    def test_count_dislikes_return_when_no_dislikes(self):
        self.assertEqual(self.user5.count_question_dislikes(), 0)
        self.assertEqual(self.user5.count_answer_dislikes(), 0)

    def test_count_karma_return_when_no_rating(self):
        user_karma = self.user5.count_karma()
        self.assertEqual(user_karma, 0)


class TestCountRatedHimselfIsNotCountedToRating(APITestCase):
    """
    Проверяем, что количество ответов, которые создал пользователь
    по отношению к своему вопросу и оценил как решенный не считается в карме.
    """
    def setUp(self):
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', is_active=True)
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq', is_active=True)
        self.user3 = NewUser.objects.create_user(email='testuser3@gmail.com', user_name='testuser3',
                                                 password='Ax6!a7OpNvq', is_active=True)

        self.tag = ThemeTag.objects.create(tag_name=f'django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user, is_solved=True)
        self.question.tags.add(self.tag)

        self.question2 = Question.objects.create(title='Заголовок', content='Контент', user=self.user2, is_solved=True)
        self.question2.tags.add(self.tag)

        self.question3 = Question.objects.create(title='Заголовок', content='Контент', user=self.user3, is_solved=True)
        self.question3.tags.add(self.tag)

        self.question4 = Question.objects.create(title='Заголовок', content='Контент', user=self.user3)
        self.question4.tags.add(self.tag)

        self.answer = QuestionAnswer.objects.create(question=self.question, user=self.user, answer='Ответ',
                                                    is_solving=True)

        self.answer2 = QuestionAnswer.objects.create(question=self.question2, user=self.user2, answer='Ответ',
                                                     is_solving=True)
        self.answer3 = QuestionAnswer.objects.create(question=self.question3, user=self.user2, answer='Ответ',
                                                     is_solving=True)
        self.answer4 = QuestionAnswer.objects.create(question=self.question4, user=self.user2, answer='Ответ')

    def test_count_user(self):
        """
        Свой ответ пользователя на свой вопрос - решающий.
        """
        self.assertEqual(self.user.get_amount_question_solved(), 0)
        self.assertEqual(self.user.count_karma(), 0)

    def test_count_user_2(self):
        """
        Два решающих ответа на два вопроса, один вопрос свой, другой нет,
        и один нерешающий ответ.
        """
        self.assertEqual(self.user2.get_amount_question_solved(), 1)
        self.assertEqual(self.user2.count_karma(), 10)
