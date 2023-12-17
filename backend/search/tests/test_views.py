from accounts.models import NewUser
from django.urls import reverse
from forum.models import Question, ThemeTag
from rest_framework import status
from rest_framework.test import APITestCase


class TestSearchListAPIView(APITestCase):

    def setUp(self):
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq')

        self.tag = ThemeTag.objects.create(tag_name='django')
        self.tag2 = ThemeTag.objects.create(tag_name='react')
        self.tag3 = ThemeTag.objects.create(tag_name='math')
        self.tag4 = ThemeTag.objects.create(tag_name='design')
        self.tag5 = ThemeTag.objects.create(tag_name='django-rest-framework')

        self.question = Question.objects.create(title='Создание API view с помощью django',
                                                content='Помогите, в чем отличие между APIView и GenericAPIView',
                                                user=self.user2)
        self.question.tags.add(self.tag, self.tag5)

        self.question2 = Question.objects.create(title='Что освоить из JS перед изучением React',
                                                 content='На сколько хорошо нужно знать JS, чтобы '
                                                         'начать изучать React. В каких темах надо '
                                                         'разбираться',
                                                 user=self.user2)
        self.question2.tags.add(self.tag2)

        self.question3 = Question.objects.create(title='Математическая реализация алгоритма '
                                                       'теории графов с использованием django rest',
                                                 content='Надо получать данные от пользователя '
                                                         'и расчетать путь из A в B ',
                                                 user=self.user2)
        self.question3.tags.add(self.tag5, self.tag3)

        self.question4 = Question.objects.create(title='Заголовок4', content='Контент4', user=self.user2)
        self.question4.tags.add(self.tag)

        self.question5 = Question.objects.create(title='Заголовок5', content='Контент5', user=self.user)
        self.question5.tags.add(self.tag, self.tag2)

        self.url = reverse('search-list')

        self.data = {'q': 'django'}

    def test_status_code(self):
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_data(self):
    #     response = self.client.get(self.url, data=self.data)
    #     print(response.content.decode())
