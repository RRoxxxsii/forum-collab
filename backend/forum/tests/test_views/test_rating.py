import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerRating, QuestionRating, ThemeTag)


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


class TestObjRatedByUser(APITestCase):

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

    def test_question_liked_or_disliked(self):
        """
        Тестируем, считается ли вопрос оцененным, несмотря на то, что пользователь
        не лайкал и не дизлайкал.
        """
        response = self.client.get(reverse('question-detail', kwargs={'pk': self.question.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, False)
        self.assertEqual(user_disliked, False)

    def test_question_liked_by_a_user(self):
        """
        Тестируем, считается ли вопрос лайкнутым пользователем.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # fetch вопроса
        response = self.client.get(reverse('question-detail', kwargs={'pk': self.question.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, True)
        self.assertEqual(user_disliked, False)

    def test_question_disliked_by_a_user(self):
        """
        Тестируем, считается ли вопрос дизлайкнутым пользователем.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.question.pk})
        self.client.get(f'{url}?model=question')

        # fetch вопроса
        response = self.client.get(reverse('question-detail', kwargs={'pk': self.question.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, False)
        self.assertEqual(user_disliked, True)

    def test_answer_liked_by_a_user(self):
        """
        Тестируем, считается ли ответ лайкнутым пользователем.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-like', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')

        # fetch вопроса
        response = self.client.get(reverse('answer-detail', kwargs={'pk': self.answer.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, True)
        self.assertEqual(user_disliked, False)

    def test_answer_disliked_by_a_user(self):
        """
        Тестируем, считается ли ответ дизлайкнутым пользователем.
        """
        self.client.force_authenticate(self.user)
        url = reverse('like-dislike-dislike', kwargs={'pk': self.answer.pk})
        self.client.get(f'{url}?model=answer')

        # fetch вопроса
        response = self.client.get(reverse('answer-detail', kwargs={'pk': self.answer.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, False)
        self.assertEqual(user_disliked, True)

    def test_anonymous_user_request(self):
        """
        Запрос от анонимного пользователя.
        """
        # fetch вопроса
        response = self.client.get(reverse('question-detail', kwargs={'pk': self.question.pk}))
        content = json.loads(response.content.decode())
        rating = content.get('rating')
        user_liked, user_disliked = rating.get('is_liked'), rating.get('is_disliked')
        self.assertEqual(user_liked, False)
        self.assertEqual(user_disliked, False)


class TestMarkAnswerAsSolving(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                     answer='Изначальный ответ2...', is_solving=True)

        self.url = reverse('mark-answer-solving', kwargs={'pk': self.answer.pk})

    def test_vote_not_authenticated(self):
        """
        Пользователь не аутентифицирован. Возвращает ошибку.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vote_not_owner(self):
        """
        Пользователь аутентифицирован, но не является владельцем вопроса. Возвращает ошибку.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vote(self):
        """
        Пользователь аутентифицирован. Ответ становится отмеченным как решающий.
        """
        self.client.force_authenticate(self.user)
        self.assertFalse(self.answer.is_solving)
        self.client.get(self.url)
        self.answer.refresh_from_db()
        self.assertTrue(self.answer.is_solving)

    def test_unvote(self):
        """
        Убираем голос с ответа.
        """
        self.client.force_authenticate(self.user)

        # Сначала ставим is_solving=True
        self.client.get(self.url)
        self.answer.refresh_from_db()
        self.assertTrue(self.answer.is_solving)

        # Ставим is_solving=False
        self.client.get(self.url)
        self.answer.refresh_from_db()
        self.assertFalse(self.answer.is_solving)

    def test_vote_for_another_answer(self):
        """
        Голос за ответ, хотя на другой ответ уже стоит. Ожидается снятие голоса с ответа
        и становление голоса на новый ответ.
        """
        self.client.force_authenticate(self.user)
        self.assertFalse(self.answer.is_solving)
        self.assertTrue(self.answer2.is_solving)
        self.client.get(self.url)

        self.answer.refresh_from_db()
        self.answer2.refresh_from_db()

        self.assertTrue(self.answer.is_solving)
        self.assertFalse(self.answer2.is_solving)


class TestQuestionMarkedAsSolved(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                     answer='Изначальный ответ2...', is_solving=False)

        self.url = reverse('mark-answer-solving', kwargs={'pk': self.answer.pk})
        self.url2 = reverse('mark-answer-solving', kwargs={'pk': self.answer2.pk})

    def test_vote(self):
        """
        Вопрос становится отмеченным как решенный.
        """
        self.client.force_authenticate(self.user)
        self.assertFalse(self.question.is_solved)
        self.client.get(self.url)
        self.question.refresh_from_db()

        self.assertTrue(self.question.is_solved)

    def test_unvote(self):
        """
        Убираем голос с ответа.
        """
        self.client.force_authenticate(self.user)

        # Сначала ставим is_solving=True
        self.client.get(self.url)
        self.question.refresh_from_db()
        self.assertTrue(self.question.is_solved)

        # Ставим is_solved=False
        self.client.get(self.url)
        self.question.refresh_from_db()

        self.assertFalse(self.question.is_solved)

    def test_vote_for_another_answer(self):
        """
        Ставим голос за другой ответ и проверяем, сохранился ли статус вопроса как решенного
        и поменялся ли статус первого ответа как не решающего, а второго как решаюшего.
        """
        self.client.force_authenticate(self.user)
        self.assertFalse(self.question.is_solved)

        self.client.get(self.url)

        self.question.refresh_from_db()
        self.assertTrue(self.question.is_solved, True)

        self.client.get(self.url2)
        self.assertTrue(self.question.is_solved)
        self.question.refresh_from_db()

        self.answer.refresh_from_db()
        self.answer2.refresh_from_db()

        self.assertFalse(self.answer.is_solving)
        self.assertTrue(self.answer2.is_solving)


class TestMarkAnswerAsSolvingNotification(APITestCase):
    """
    Тестируем мприход уведомления после создания вопроса.
    """
    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        self.question.tags.add(self.tag)
        self.answer = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user2, question=self.question,
                                                     answer='Изначальный ответ2...', is_solving=True)

        self.url = reverse('mark-answer-solving', kwargs={'pk': self.answer.pk})

    def test_get_notified(self):
        self.client.force_authenticate(self.user)
        self.assertFalse(self.answer.is_solving)
        self.client.get(self.url)
        self.assertEqual(len(self.user2.notifications.all()), 1)


class TestUserComplain(APITestCase):

    def setUp(self):
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.tag = ThemeTag.objects.create(tag_name='django')

        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.question.tags.add(self.tag)

        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')

        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer, comment='Комментарий')

        self.url_question = reverse('complain', kwargs={'content_id': self.question.pk,
                                                        'content_type': 'question'})
        self.url_answer = reverse('complain', kwargs={'content_id': self.answer.pk,
                                                      'content_type': 'answer'})
        self.url_comment = reverse('complain', kwargs={'content_id': self.comment.pk,
                                                       'content_type': 'comment'})

        self.wrong_url = reverse('complain', kwargs={'content_id': self.comment.pk,
                                                     'content_type': 'wrong-content_type'})

    def test_complain_on_question_status_code(self):
        """
        Тестируем код ответа при создании жалобы на вопрос.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.patch(self.url_question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complain_on_question_user_added(self):
        """
        Тестируем обновление данных при создании жалобы на вопрос.
        """
        self.client.force_authenticate(self.user2)
        self.client.patch(self.url_question)
        self.assertEqual(len(self.question.rating.users_complained.all()), 1)

    def test_complain_on_answer_status_code(self):
        """
        Тестируем код ответа при создании жалобы на ответ.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.patch(self.url_answer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complain_on_answer_user_added(self):
        """
        Тестируем обновление данных при создании жалобы на ответ.
        """
        self.client.force_authenticate(self.user2)
        self.client.patch(self.url_answer)
        self.assertEqual(len(self.answer.rating.users_complained.all()), 1)

    def test_complain_on_comment_status_code(self):
        """
        Тестируем код ответа при создании жалобы на комментарий.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.patch(self.url_comment)
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complain_on_comment_user_added(self):
        """
        Тестируем обновление данных при создании жалобы на комментарий.
        """
        self.client.force_authenticate(self.user2)
        self.client.patch(self.url_comment)
        self.assertEqual(len(self.comment.rating.users_complained.all()), 1)

    def test_wrong_content_type_url_status_code(self):
        """
        Тестируем код ответа при создании жалобы с некорректным типом контента.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.patch(self.wrong_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
