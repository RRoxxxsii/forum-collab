import datetime
import io
import json
import random

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from faker import Faker
from PIL import Image
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages, ThemeTag)
from forum.serializers import DetailQuestionSerializer


def reformat(obj):
    obj = str(obj).replace(' ', '_').strip('<').replace('>', '')
    return obj


def generate_photo_file(file_name: str):
    # Create an in-memory image
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))

    # Save the image to a BytesIO buffer
    file = io.BytesIO()
    image.save(file, 'png')
    file.name = f'{file_name}.png'

    # Create a SimpleUploadedFile object from the BytesIO buffer
    uploaded_file = SimpleUploadedFile(file.name, file.getvalue())

    return uploaded_file


class TestQuestionDetailAPITestCase(APITestCase):

    def setUp(self) -> None:
        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        fake = Faker()

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        question_image = generate_photo_file(file_name=fake.unique.file_name)
        question_image2 = generate_photo_file(file_name=fake.unique.file_name)
        question_image_obj = QuestionImages.objects.create(image=question_image, parent=self.question)
        question_image_obj2 = QuestionImages.objects.create(image=question_image2, parent=self.question)
        self.question.tags.add(self.tag)
        self.question.question_images.add(question_image_obj, question_image_obj2)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                     answer='Изначальный ответ2...')
        answer_image = generate_photo_file(file_name=fake.unique.file_name)
        answer_image_obj = QuestionAnswerImages.objects.create(image=answer_image, parent=self.answer)
        self.answer.answer_images.add(answer_image_obj)

        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='agagag')
        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='bfbd')

        serialized_data = DetailQuestionSerializer(self.question, context={'request': request})
        self.data_json = json.dumps(serialized_data.data, indent=4, ensure_ascii=False)

        # получаем текущее время
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expected_data = {
            "id": 1,
            "user": {
                "id": 1,
                "email": "testuser@gmail.com",
                "user_name": "testuser",
                "about": "",
                "profile_image": None,
                "is_active": True,
                "is_banned": False,
                "email_confirmed": False,
                "created": current_datetime
            },
            "title": "Заголовок",
            "content": "Контент",
            "answers_amount": 2,
            "is_solved": False,
            "creation_date": current_datetime,
            "updated_date": current_datetime,
            "images": [
                {
                    "id": question_image_obj.id,
                    "image": f"http://testserver/media/{reformat(question_image2)}",
                    "alt_text": question_image_obj2.alt_text
                },
                {
                    "id": question_image_obj2.id,
                    "image": f"http://testserver/media/{reformat(question_image2)}",
                    "alt_text": question_image_obj2.alt_text
                }
            ],
            "rating": {
                "id": 1,
                "is_liked": False,
                "is_disliked": False,
                "like_amount": 0,
                "dislike_amount": 0,
                "question": 1,
                "users_liked": [],
                "users_disliked": []
            },
            "answers": [
                {
                    "id": 1,
                    "question": 1,
                    "user": {
                        "id": 1,
                        "email": "testuser@gmail.com",
                        "user_name": "testuser",
                        "about": "",
                        "profile_image": None,
                        "is_active": True,
                        "is_banned": False,
                        "email_confirmed": False,
                        "created": current_datetime
                    },
                    "answer": "Изначальный ответ...",
                    "is_solving": False,
                    "creation_date": current_datetime,
                    "updated_date": current_datetime,
                    "rating": {
                        "id": 1,
                        "is_liked": False,
                        "is_disliked": False,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": 1,
                        "users_liked": [],
                        "users_disliked": []
                    },
                    "images": [
                        {
                            "id": answer_image_obj.id,
                            "image": f"http://testserver/media/{reformat(answer_image)}",
                            "alt_text": answer_image_obj.alt_text
                        }
                    ],
                    "comments": [
                        {
                            "id": 1,
                            "user": {
                                "id": 1,
                                "email": "testuser@gmail.com",
                                "user_name": "testuser",
                                "about": "",
                                "profile_image": None,
                                "is_active": True,
                                "is_banned": False,
                                "email_confirmed": False,
                                "created": current_datetime
                            },
                            "comment": "agagag",
                            "creation_date": current_datetime,
                            "updated_date": current_datetime,
                            "question_answer": 1,
                            "parent": None
                        },
                        {
                            "id": 2,
                            "user": {
                                "id": 1,
                                "email": "testuser@gmail.com",
                                "user_name": "testuser",
                                "about": "",
                                "profile_image": None,
                                "is_active": True,
                                "is_banned": False,
                                "email_confirmed": False,
                                "created": current_datetime
                            },
                            "comment": "bfbd",
                            "creation_date": current_datetime,
                            "updated_date": current_datetime,
                            "question_answer": 1,
                            "parent": None
                        }
                    ]
                },
                {
                    "id": 2,
                    "question": 1,
                    "user": {
                        "id": 1,
                        "email": "testuser@gmail.com",
                        "user_name": "testuser",
                        "about": "",
                        "profile_image": None,
                        "is_active": True,
                        "is_banned": False,
                        "email_confirmed": False,
                        "created": current_datetime
                    },
                    "answer": "Изначальный ответ2...",
                    "is_solving": False,
                    "creation_date": current_datetime,
                    "updated_date": current_datetime,
                    "rating": {
                        "id": 2,
                        "is_liked": False,
                        "is_disliked": False,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": 2,
                        "users_liked": [],
                        "users_disliked": []
                    },
                    "images": [],
                    "comments": []
                }
            ],
            "tags": [
                {
                    "tag_name": "django",
                    "is_relevant": True,
                    "is_user_tag": False
                }
            ]
        }

        self.expected_data_json = json.dumps(expected_data, indent=4, ensure_ascii=False)

    def test_ok(self):
        """
        Тест может падать из-за различия в одну секунду или
        небольших различиях в названии файлов, которые в рамках теста НЕКРИТИЧНЫ.
        В таком случае тест необходимо перезапустить отдельно.
        Или сравнить вручную.
        """
        # print(self.expected_data_json)
        # print('-' * 100)
        # print(self.data_json)
        self.assertEqual(self.data_json, self.expected_data_json)
