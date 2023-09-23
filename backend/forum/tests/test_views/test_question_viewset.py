import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages, ThemeTag)
from forum.tests.test_serializers import generate_photo_file


class TestQuestionViewSet(APITestCase):

    def setUp(self) -> None:

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        question_image = generate_photo_file()
        question_image2 = generate_photo_file()
        question_image_obj = QuestionImages.objects.create(image=question_image, parent=self.question)
        question_image_obj2 = QuestionImages.objects.create(image=question_image2, parent=self.question)
        self.question.tags.add(self.tag)
        self.question.question_images.add(question_image_obj, question_image_obj2)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        answer_image = generate_photo_file()
        answer_image_obj = QuestionAnswerImages.objects.create(image=answer_image, parent=self.answer)
        self.answer.answer_images.add(answer_image_obj)

        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='agagag')
        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='bfbd')

        self.url = reverse('question-list')
        self.detail_question_url = reverse('question-detail', kwargs={'pk': self.question.id})

    def test_list_questions_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_question_content(self):
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        self.assertIn('rating', *content)
        self.assertIn('tags', *content)

    def test_detail_question_status_code(self):
        response = self.client.get(self.detail_question_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_question_content(self):
        response = self.client.get(self.detail_question_url)
        content = json.loads(response.content.decode())
        content_answers = content.get('answers')

        self.assertIn('answers', content)
        self.assertIn('images', content)
        self.assertIn('rating', content)
        self.assertIn('tags', content)

        self.assertIn('comments', *content_answers)
        self.assertIn('images', *content_answers)
        self.assertIn('rating', *content_answers)


class TestQuestionListLimit(APITestCase):

    def setUp(self) -> None:
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.question2 = Question.objects.create(title='Заголовок2', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        question_image = generate_photo_file()
        question_image2 = generate_photo_file()
        question_image_obj = QuestionImages.objects.create(image=question_image, parent=self.question)
        question_image_obj2 = QuestionImages.objects.create(image=question_image2, parent=self.question)
        self.question.tags.add(self.tag)
        self.question.question_images.add(question_image_obj, question_image_obj2)

        self.url = reverse('question-list')

    def test_limit_1(self):
        """
        Тестирование количества возвращенных вопросов при лимите равном 1.
        """
        response = self.client.get(f'{self.url}?limit=1')
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), 1)

    def test_limit_without_query_params(self):
        """
        Тестируем без передачи параметров запроса.
        """
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), 2)
