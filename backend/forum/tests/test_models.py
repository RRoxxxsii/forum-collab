from accounts.models import NewUser
from forum.models import (Question, QuestionAnswer, QuestionAnswerRating,
                          QuestionRating, ThemeTag)
from forum.services import LikeDislikeService
from rest_framework.test import APITestCase


class TestThemeTagMakingTagRelevant(APITestCase):
    """
    Тестирует изменение статуса тега на релевантный.
    """

    def setUp(self) -> None:
        self.tag1 = ThemeTag.objects.create(tag_name='django', is_relevant=False, is_user_tag=True)
        self.tag2 = ThemeTag.objects.create(tag_name='react', is_relevant=False)
        self.tag3 = ThemeTag.objects.create(tag_name='python', is_relevant=False)
        self.tag4 = ThemeTag.objects.create(tag_name='nextjs', is_relevant=False)
        self.tag5 = ThemeTag.objects.create(tag_name='C#', is_relevant=False)
        self.tag6 = ThemeTag.objects.create(tag_name='Java', is_relevant=False)
        self.tag7 = ThemeTag.objects.create(tag_name='django-rest-framework', is_relevant=False)

        for i in range(9):
            question = Question.objects.create(title=f'Заголовок{i}', content=f'Контент{i}')
            question.tags.add(self.tag1.id)

    def test_tag_relevant(self):
        self.assertFalse(self.tag1.is_relevant)  # 9 вопросов по тегу, нерелевантен

        # Создаем еще один вопрос
        self.question = Question.objects.create(title='Заголовок12', content='Контент12')
        self.question.tags.add(self.tag1.id)
        self.question.save()
        self.tag1.refresh_from_db()

        self.assertTrue(self.tag1.is_relevant)


class TestLikeDislike(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.tag = ThemeTag.objects.create(tag_name='django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.question.tags.add(self.tag)

        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')

    def test_like_question(self):
        LikeDislikeService().like(self.user, obj=self.question)
        likes = QuestionRating.objects.all().first()
        self.assertEqual(likes.like_amount, 1)

    def test_dislike_question(self):
        likes = QuestionRating.objects.all().first()
        LikeDislikeService().dislike(self.user, obj=self.question)
        likes = QuestionRating.objects.all().first()
        self.assertEqual(likes.dislike_amount, 1)

    def test_like_answer(self):
        LikeDislikeService().like(self.user, obj=self.answer)
        likes = QuestionAnswerRating.objects.all().first()
        self.assertEqual(likes.like_amount, 1)

    def test_dislike_answer(self):
        LikeDislikeService().dislike(self.user, obj=self.answer)
        likes = QuestionAnswerRating.objects.all().first()
        self.assertEqual(likes.dislike_amount, 1)
