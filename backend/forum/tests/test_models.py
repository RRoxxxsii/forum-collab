from rest_framework.test import APITestCase

from forum.models import Question, ThemeTag


class TestThemeTagMakingTagRelevant(APITestCase):
    """
    Тестирует изменение статуса тега на релевантный.
    """

    def setUp(self) -> None:
        self.tag1 = ThemeTag.objects.create(tag='django', is_relevant=False, is_user_tag=True)
        self.tag2 = ThemeTag.objects.create(tag='react', is_relevant=False)
        self.tag3 = ThemeTag.objects.create(tag='python', is_relevant=False)
        self.tag4 = ThemeTag.objects.create(tag='nextjs', is_relevant=False)
        self.tag5 = ThemeTag.objects.create(tag='C#', is_relevant=False)
        self.tag6 = ThemeTag.objects.create(tag='Java', is_relevant=False)
        self.tag7 = ThemeTag.objects.create(tag='django-rest-framework', is_relevant=False)

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
