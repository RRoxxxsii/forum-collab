import datetime
import io
import json

import pytz
from django.conf import settings
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


def convert_datetime(dt):
    moscow_tz = pytz.timezone('Europe/Moscow')

    return dt.replace(tzinfo=pytz.utc).astimezone(moscow_tz).strftime("%Y-%m-%d %H:%M:%S")


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
        question_image = generate_photo_file(file_name=fake.unique.file_name())
        question_image2 = generate_photo_file(file_name=fake.unique.file_name())
        question_image_obj = QuestionImages.objects.create(image=question_image, parent=self.question)
        question_image_obj2 = QuestionImages.objects.create(image=question_image2, parent=self.question)
        self.question.tags.add(self.tag)
        self.question.question_images.add(question_image_obj, question_image_obj2)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                     answer='Изначальный ответ2...')
        answer_image = generate_photo_file(file_name=fake.unique.file_name())
        answer_image_obj = QuestionAnswerImages.objects.create(image=answer_image, parent=self.answer)
        self.answer.answer_images.add(answer_image_obj)

        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='agagag')
        self.comment2 = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='bfbd')

        serialized_data = DetailQuestionSerializer(self.question, context={'request': request})
        self.data_json = json.dumps(serialized_data.data, indent=4, ensure_ascii=False)

        expected_data = {
            "id": self.question.pk,
            "user": {
                "id": self.user.pk,
                "email": "testuser@gmail.com",
                "user_name": "testuser",
                "about": "",
                "profile_image": None,
                "is_active": True,
                "is_banned": False,
                "email_confirmed": False,
                "created": str(convert_datetime(self.user.created))
            },
            "title": "Заголовок",
            "content": "Контент",
            "answers_amount": 2,
            "is_solved": False,
            "creation_date": str(convert_datetime(self.question.creation_date)),
            "updated_date": str(convert_datetime(self.question.updated_date)),
            "images": [
                {
                    "id": question_image_obj.id,
                    "image": f"http://testserver/media/{question_image_obj}",
                    "alt_text": question_image_obj2.alt_text
                },
                {
                    "id": question_image_obj2.id,
                    "image": f"http://testserver/media/{question_image_obj2}",
                    "alt_text": question_image_obj2.alt_text
                }
            ],
            "rating": {
                "id": self.question.pk,
                "is_liked": False,
                "is_disliked": False,
                "like_amount": 0,
                "dislike_amount": 0,
                "question": self.question.pk,
                "users_liked": [],
                "users_disliked": []
            },
            "answers": [
                {
                    "id": self.answer.pk,
                    "question": self.question.pk,
                    "user": {
                        "id": self.user.pk,
                        "email": "testuser@gmail.com",
                        "user_name": "testuser",
                        "about": "",
                        "profile_image": None,
                        "is_active": True,
                        "is_banned": False,
                        "email_confirmed": False,
                        "created": str(convert_datetime(self.user.created))
                    },
                    "answer": "Изначальный ответ...",
                    "is_solving": False,
                    "creation_date": str(convert_datetime(self.answer.creation_date)),
                    "updated_date": str(convert_datetime(self.answer.updated_date)),
                    "rating": {
                        "id": self.answer.pk,
                        "is_liked": False,
                        "is_disliked": False,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": self.answer.pk,
                        "users_liked": [],
                        "users_disliked": []
                    },
                    "images": [
                        {
                            "id": answer_image_obj.id,
                            "image": f"http://testserver/media/{answer_image_obj}",
                            "alt_text": answer_image_obj.alt_text
                        }
                    ],
                    "comments": [
                        {
                            "id": self.comment.pk,
                            "user": {
                                "id": self.user.pk,
                                "email": "testuser@gmail.com",
                                "user_name": "testuser",
                                "about": "",
                                "profile_image": None,
                                "is_active": True,
                                "is_banned": False,
                                "email_confirmed": False,
                                "created": str(convert_datetime(self.user.created))
                            },
                            "comment": "agagag",
                            "creation_date": str(convert_datetime(self.comment.creation_date)),
                            "updated_date": str(convert_datetime(self.comment.updated_date)),
                            "question_answer": self.answer.pk,
                            "parent": None
                        },
                        {
                            "id": self.comment2.pk,
                            "user": {
                                "id": self.user.pk,
                                "email": "testuser@gmail.com",
                                "user_name": "testuser",
                                "about": "",
                                "profile_image": None,
                                "is_active": True,
                                "is_banned": False,
                                "email_confirmed": False,
                                "created": str(convert_datetime(self.user.created))
                            },
                            "comment": "bfbd",
                            "creation_date": str(convert_datetime(self.comment2.creation_date)),
                            "updated_date": str(convert_datetime(self.comment2.updated_date)),
                            "question_answer": self.answer.pk,
                            "parent": None
                        }
                    ]
                },
                {
                    "id": self.answer2.pk,
                    "question": self.question.pk,
                    "user": {
                        "id": self.user.pk,
                        "email": "testuser@gmail.com",
                        "user_name": "testuser",
                        "about": "",
                        "profile_image": None,
                        "is_active": True,
                        "is_banned": False,
                        "email_confirmed": False,
                        "created": str(convert_datetime(self.user.created))
                    },
                    "answer": "Изначальный ответ2...",
                    "is_solving": False,
                    "creation_date": str(convert_datetime(self.answer2.creation_date)),
                    "updated_date": str(convert_datetime(self.answer2.updated_date)),
                    "rating": {
                        "id": self.answer2.pk,
                        "is_liked": False,
                        "is_disliked": False,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": self.answer2.pk,
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
        Тест может падать из-за небольших различий (во времени).
        В таком случае тест необходимо перезапустить отдельно.
        Или сравнить вручную.
        """
        # print(self.expected_data_json)
        # print('-' * 100)
        # print(self.data_json)
        self.assertEqual(self.data_json, self.expected_data_json)
