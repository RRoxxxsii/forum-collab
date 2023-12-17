from __future__ import annotations

import random

from accounts.models import NewUser
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import QuerySet
from faker import Faker
from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages, ThemeTag)
from forum.tests.test_serializers import generate_photo_file
from notifications.utils import notify


class BaseAnswerQuestionHelperMixin:
    """
    Миксин реализующий метод создания рейтинга. Наследуется в классах, где
    необходимо создавать рейтинг.
    """

    def _create_rating(self, instance: [Question | QuestionAnswer], users_sorted: QuerySet[NewUser]):
        users_liked = list(users_sorted[:random.randint(0, self.users.count())])
        users_disliked = []
        for user in users_sorted[:random.randint(0, self.users.count())]:
            if user not in users_liked:
                users_disliked.append(user)

        instance.rating.users_liked.add(*users_liked)
        instance.rating.users_disliked.add(*users_disliked)
        instance.rating.like_amount = len(users_liked)
        instance.rating.dislike_amount = len(users_disliked)
        instance.rating.save()
        instance.save()


class QuestionHelper(BaseAnswerQuestionHelperMixin):
    """
    Класс-помощник для создания вопросов.
    """

    def __init__(self, questions_amount, users, tags):
        self.questions_amount = questions_amount
        self.users = users
        self.tags = tags
        self.fake = Faker(['ru_RU'])

    def create_questions(self):
        for _ in range(self.questions_amount):
            users_sorted = self.users.order_by('?')
            tags_sorted = self.tags.order_by('?')[:random.randint(1, 5)]

            question = Question.objects.create(
                user=users_sorted.first(),
                title=self.fake.text(max_nb_chars=200),
                content=self.fake.paragraph(nb_sentences=7),
                is_solved=self.fake.pybool()
            )

            for tag in tags_sorted:
                question.tags.add(tag)
            question.save()

            self._create_question_images(question)
            self._create_rating(instance=question, users_sorted=users_sorted)

        questions = Question.objects.all()

        return questions

    def _create_question_images(self, question):
        for _ in range(random.randint(0, 3)):
            flag = random.randint(0, 1)
            image = generate_photo_file(file_name=self.fake.file_name)

            question_image = QuestionImages.objects.create(
                parent=question,
                image=image
            )
            if flag:
                question_image.alt = self.fake.text(max_nb_chars=200)
            question_image.save()


class AnswerHelper(BaseAnswerQuestionHelperMixin):
    """
    Класс-помощник для создания ответов.
    """

    def __init__(self, users, questions):
        self.users = users
        self.questions = questions
        self.fake = Faker(['ru_RU'])

    def create_answers(self):
        for question in self.questions:
            flag = random.randint(0, 1)
            users_sorted = self.users.order_by('?')

            if flag:
                answer = QuestionAnswer.objects.create(
                    question=question, answer=self.fake.paragraph(nb_sentences=7)
                )
                user_identified = random.randint(0, 1)

                if user_identified:
                    answer.user = users_sorted.first()

                    notify(sender=answer.user, receiver=question.user,
                           text='ответил на ваш вопрос',
                           action_obj=answer, target=question)
                    answer.save()

                self._create_answer_images(answer=answer)
                self._create_rating(instance=answer, users_sorted=users_sorted)

        answers = QuestionAnswer.objects.all()

        return answers

    def _create_answer_images(self, answer):
        generate_image = random.randint(0, 1)
        if generate_image:

            image = generate_photo_file(file_name=self.fake.file_name)
            QuestionAnswerImages.objects.create(
                parent=answer,
                image=image
            )


class Helper(AnswerHelper, QuestionHelper):
    """
    Класс помощник для создания тегов, пользователей и комментариев.
    """

    def create_tags(self, tags_amount):
        fake = Faker(['ru_RU'])

        for _ in range(tags_amount):
            ThemeTag.objects.create(tag_name=fake.unique.word(), is_relevant=fake.pybool(),
                                    is_user_tag=fake.pybool(), descriptions=fake.paragraph())

        tags = ThemeTag.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число тегов: {tags.count()}.'))

        return tags

    def create_users(self, users_amount):
        fake = Faker(['ru_RU'])

        NewUser.objects.create_superuser(
                email='testadmin@example.com', password='1234',
                user_name='root'
            )

        for _ in range(users_amount):

            user = NewUser.objects.create(
                email=fake.unique.email(), password='12345',
                user_name=fake.unique.name(),
                is_banned=fake.pybool(), is_active=fake.pybool(),
                email_confirmed=fake.pybool()
            )
            is_profile_img = random.randint(0, 1)
            is_about = random.randint(0, 1)

            if is_profile_img:
                image = generate_photo_file(file_name=fake.file_name)
                user.profile_image = image

            if is_about:
                user.about = fake.paragraph()

            user.save()

        users = NewUser.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число пользователей: {users.count()}.'))

        return users

    def create_comments(self, answers, users):
        fake = Faker(['ru_RU'])

        for answer in answers:
            flag = random.randint(0, 1)
            users_ = users.order_by('?')

            if flag:
                user_identified = random.randint(0, 1)
                comment = AnswerComment.objects.create(
                    comment=fake.sentence(nb_words=10, variable_nb_words=False),
                    question_answer=answer
                )

                if user_identified:
                    comment.user = users_.first()

                    if answer.user:
                        notify(sender=comment.user, receiver=answer.user,
                               text='прокомментировал ваш ответ',
                               action_object=comment, target=answer)

                    comment.save()

        comments = AnswerComment.objects.all()
        return comments


class Command(BaseCommand, Helper):
    help = 'Создание фикстур'

    @transaction.atomic
    def handle(self, *args, **options):
        tags = self.create_tags(tags_amount=15)
        users = self.create_users(users_amount=20)

        q = QuestionHelper(questions_amount=50, users=users, tags=tags)
        questions = q.create_questions()
        self.stdout.write(self.style.SUCCESS(f'Число вопросов: {questions.count()}.'))

        a = AnswerHelper(users=users, questions=questions)
        answers = a.create_answers()
        self.stdout.write(self.style.SUCCESS(f'Число ответов: {answers.count()}.'))

        comments = self.create_comments(answers=answers, users=users)
        self.stdout.write(self.style.SUCCESS(f'Число комментариев: {comments.count()}.'))
