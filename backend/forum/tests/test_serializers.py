from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import ThemeTag
from forum.serializers import AskQuestionSerializer


class TestAskQuestionSerializer(APITestCase):

    def setUp(self) -> None:
        self.tag1 = ThemeTag.objects.create(tag='django')
        self.tag2 = ThemeTag.objects.create(tag='react')
        self.tag3 = ThemeTag.objects.create(tag='python')
        self.tag4 = ThemeTag.objects.create(tag='nextjs')
        self.tag5 = ThemeTag.objects.create(tag='C#')
        self.tag6 = ThemeTag.objects.create(tag='Java')
        self.tag7 = ThemeTag.objects.create(tag='django-rest-framework')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

        self.expected_data = {
            'tag_ids': [1, 7],
            'author': 'testuser',
            'title': 'Не знаю как решить проблему',
            'content': 'Какой-то контент...'
        }

    def test_more_then_five_tags_in_serializer(self):
        """
        Тестирует, что возбуждается ошибка валидации при количестве тегов больше 5
        """
        try:
            AskQuestionSerializer(data={'tag_ids': [self.tag1, self.tag2, self.tag3,
                                                    self.tag4, self.tag5, self.tag6],
                                        'author': self.user,
                                        'title': 'Не знаю как решить проблему',
                                        'content': 'Какой-то контент..'})
        except ValidationError:
            assert True
        else:
            assert False

    def test_serializer_ok(self):
        data = AskQuestionSerializer(data={'tag_ids': [self.tag1, self.tag2],
                                           'author': self.user,
                                           'title': 'Не знаю как решить проблему',
                                           'content': 'Какой-то контент..'})

        print(data)
        print('----------------------')
        print(self.expected_data)
        self.assertEqual(data, self.expected_data)
