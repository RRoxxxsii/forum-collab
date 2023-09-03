from accounts.models import NewUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import (Question, QuestionAnswer, QuestionAnswerRating,
                          QuestionRating, ThemeTag)


class TestLikeDislikeAPIView(APITestCase):

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

    def test_user_not_authenticated(self):
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_author(self):
        """
        Пользователь оценивает свою запись. Действие должно быть недоступно.
        """
        self.client.force_authenticate(self.user2)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_question_status_code(self):
        """
        Тестируем код ответа при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_question_created_question(self):
        """
        Тестируем создание лайка при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_question_status_code(self):
        """
        Тестируем код ответа при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        response = self.client.get(f'{url}?model=question')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_question_created(self):
        """
        Тестируем создание дизлайка при отправке запроса к вопросу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 0)
        self.assertEqual(rating.dislike_amount, 1)

    def test_like_answer_status_code(self):
        """
        Тестируем код ответа при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.answer.pk})
        response = self.client.get(f'{url}?model=answer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_answer_created(self):
        """
        Тестируем создание лайка при отправке запроса к овтету.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')
        rating = QuestionAnswerRating.objects.first()
        self.assertEqual(rating.like_amount, 1)
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_answer_status_code(self):
        """
        Тестируем код ответа при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.answer.pk})
        response = self.client.get(f'{url}?model=answer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_answer_created(self):
        """
        Тестируем создание дизлайка при отправке запроса к ответу.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')
        rating = QuestionAnswerRating.objects.first()
        self.assertEqual(rating.like_amount, 0)
        self.assertEqual(rating.dislike_amount, 1)

    def test_unlike(self):
        """
        Убираем лайк.
        """
        # Сначала ставим лайк
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)

        # Повторно отправляем запрос на этот же url, тем самым удаляя лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 0)

    def test_like_when_disliked(self):
        """
        Пользователь лайкает, когда уже стоит дизлайк.
        """
        # Создаем дизлайк для пользователя
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Cтавим лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 0)

        # Проверяем, поставился ли лайк
        self.assertEqual(rating.like_amount, 1)

    def test_undislike(self):
        """
        Убираем дизлайк.
        """
        self.client.force_authenticate(self.user)
        # Cоздаем дизлайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 1)

        # Повторно отправляем запрос на этот же url, тем самым удаляя лайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, убрался ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 0)

    def test_dislike_when_liked(self):
        """
        Пользователь ставит дизлайк, когда уже стоит лайк.
        """
        self.client.force_authenticate(self.user)
        # Ставим лайк
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли лайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.like_amount, 1)

        # Ставим дизлайк
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # Проверяем, поставился ли дизлайк
        rating = QuestionRating.objects.first()
        self.assertEqual(rating.dislike_amount, 1)