from accounts.models import NewUser
from django.urls import reverse
from faker import Faker
from forum.models import Question, QuestionImages, ThemeTag
from forum.tests.test_serializers import generate_photo_file
from rest_framework import status
from rest_framework.test import APITestCase


class TestUpdateDestroyQuestionAPIView(APITestCase):
    """
    Обновление вопроса.
    """
    def setUp(self) -> None:
        fake = Faker()

        self.tag1 = ThemeTag.objects.create(tag_name='django')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.question1 = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.question1.tags.add(self.tag1.id)

        self.question2 = Question.objects.create(title='Заголовок', content='Контент', user=self.user2)
        self.question2.tags.add(self.tag1.id)
        image = generate_photo_file(fake.unique.file_name)
        image2 = generate_photo_file(fake.unique.file_name)
        QuestionImages.objects.create(image=image, parent=self.question2)
        QuestionImages.objects.create(image=image2, parent=self.question2)

        self.url = reverse('update-question', kwargs={'pk': self.question1.id})
        self.url = reverse('update-question', kwargs={'pk': self.question2.id})
        self.data = {'content': 'Обновленный вопрос'}

    def test_update_question_not_owner(self):
        """
        Обновление вопроса не являясь автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_question_not_authenticated(self):
        """
        Пользователь не аутентифицирован.
        """
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_question(self):
        """
        Обновление ответа с помощью метода put.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_with_existed_photos(self):
        """
        Обновление тега, для которого уже существуют фотографиями.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_question_not_owner(self):
        """
        Get-запрос на вопрос, не являясь автором. Ожидается открытый доступ.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_authenticated(self):
        """
        Get-запрос, не аутентифицированный.
        """
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question_not_owner(self):
        """
        Удаление вопроса, не являясь его автором.
        """
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question(self):
        """
        Удаление вопроса автором.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
