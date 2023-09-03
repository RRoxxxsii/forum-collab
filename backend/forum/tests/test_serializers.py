import datetime
import io
import json
import random

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from rest_framework.test import APITestCase

from accounts.models import NewUser
from forum.models import Question, ThemeTag, QuestionImages, QuestionAnswer, QuestionAnswerImages, AnswerComment
from forum.serializers import DetailQuestionSerializer


def generate_photo_file():
    # Create an in-memory image
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))

    # Save the image to a BytesIO buffer
    file = io.BytesIO()
    image.save(file, 'png')
    file.name = f'test{random.randint(1, 1000000)}.png'

    # Create a SimpleUploadedFile object from the BytesIO buffer
    uploaded_file = SimpleUploadedFile(file.name, file.getvalue())

    return uploaded_file


class TestQuestionDetailAPITestCase(APITestCase):

    def setUp(self) -> None:
        request = RequestFactory().get('/')

        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.question = Question.objects.create(title='Заголовок', content='Контент', user=self.user)
        self.tag = ThemeTag.objects.create(tag_name='django')
        question_image = generate_photo_file()
        question_image2 = generate_photo_file()
        question_image_obj = QuestionImages.objects.create(image=question_image, parent=self.question)
        question_image_obj2 = QuestionImages.objects.create(image=question_image2, parent=self.question)
        self.question.tags.add(self.tag)
        self.question.question_images.add(question_image_obj, question_image_obj2)
        self.answer = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                    answer='Изначальный ответ...')
        self.answer2 = QuestionAnswer.objects.create(user=self.user, question=self.question,
                                                     answer='Изначальный ответ2...')
        answer_image = generate_photo_file()
        answer_image_obj = QuestionAnswerImages.objects.create(image=answer_image, parent=self.answer)
        self.answer.answer_images.add(answer_image_obj)

        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='agagag')
        self.comment = AnswerComment.objects.create(user=self.user, question_answer=self.answer,
                                                    comment='bfbd')

        serialized_data = DetailQuestionSerializer(self.question, context={'request': request})
        self.data_json = json.dumps(serialized_data.data, indent=4, ensure_ascii=False)
        expected_data = {
            "id": 1,
            "user": 1,
            "title": "Заголовок",
            "content": "Контент",
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "images": [
                "http://testserver/api/v1/forum/questions/1/",
                "http://testserver/api/v1/forum/questions/2/"
            ],
            "rating": {
                "id": 1,
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
                    "user": 1,
                    "answer": "Изначальный ответ...",
                    "is_solving": False,
                    "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "rating": {
                        "id": 1,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": 1,
                        "users_liked": [],
                        "users_disliked": []
                    },
                    "images": [
                        "http://testserver/api/v1/forum/answers/1/"
                    ],
                    "comments": [
                        {
                            "id": 1,
                            "comment": "agagag",
                            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user": 1,
                            "question_answer": 1
                        },
                        {
                            "id": 2,
                            "comment": "bfbd",
                            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user": 1,
                            "question_answer": 1
                        }
                    ]
                },
                {
                    "id": 2,
                    "question": 1,
                    "user": 1,
                    "answer": "Изначальный ответ2...",
                    "is_solving": False,
                    "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "rating": {
                        "id": 2,
                        "like_amount": 0,
                        "dislike_amount": 0,
                        "answer": 2,
                        "users_liked": [],
                        "users_disliked": []
                    },
                    "images": [],
                    "comments": []
                }
            ]
        }

        self.expected_data_json = json.dumps(expected_data, indent=4, ensure_ascii=False)

    def test_ok(self):
        self.assertEqual(self.data_json, self.expected_data_json)
