import random

from accounts.models import NewUser
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker

from forum.models import (AnswerComment, Question, QuestionAnswer,
                          QuestionAnswerImages, QuestionImages, ThemeTag)


class Helper:

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

        for _ in range(users_amount):
            NewUser.objects.create(email=fake.unique.email(), password='12345',
                                   user_name=fake.unique.name(), about=fake.paragraph(),
                                   profile_image=fake.file_name(category='image', extension='jpeg'),
                                   is_banned=fake.pybool(), is_active=fake.pybool(),
                                   email_confirmed=fake.pybool())

        users = NewUser.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число пользователей: {users.count()}.'))

        return users

    def create_questions(self, questions_amount, users, tags):
        fake = Faker(['ru_RU'])

        for _ in range(questions_amount):
            users_ = users.order_by('?')
            tags_ = tags.order_by('?')[:random.randint(1, 5)]

            question = Question.objects.create(user=users_.first(), title=fake.text(max_nb_chars=200),
                                               content=fake.paragraph(nb_sentences=7),
                                               is_solved=fake.pybool())

            for tag in tags_:
                question.tags.add(tag)
            question.save()

            for _ in range(random.randint(0, 3)):
                flag = random.randint(0, 1)
                question_image = QuestionImages.objects.create(
                    parent=question,
                    image=fake.file_name(category='image', extension='jpeg')
                )
                if flag:
                    question_image.alt = fake.text(max_nb_chars=200)
                question_image.save()

            users_liked = list(users_[:random.randint(0, users.count())])
            users_disliked = []
            for user in users_[:random.randint(0, users.count())]:
                if user not in users_liked:
                    users_disliked.append(user)

            question.rating.users_liked.add(*users_liked)
            question.rating.users_disliked.add(*users_disliked)
            question.rating.like_amount = len(users_liked)
            question.rating.dislike_amount = len(users_disliked)
            question.rating.save()
            question.save()

        questions = Question.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число вопросов: {questions.count()}.'))

        return questions

    def create_answers(self, questions, users):
        fake = Faker(['ru_RU'])

        for question in questions:
            flag = random.randint(0, 1)
            users_ = users.order_by('?')

            if flag:
                answer = QuestionAnswer.objects.create(question=question, answer=fake.paragraph(nb_sentences=7))
                user_identified = random.randint(0, 1)

                if user_identified:
                    answer.user = users_.first()
                    answer.save()

                generate_image = random.randint(0, 1)
                if generate_image:
                    QuestionAnswerImages.objects.create(
                        parent=answer,
                        image=fake.file_name(category='image', extension='jpeg')
                    )

                users_liked = list(users_[:random.randint(0, users.count())])
                users_disliked = []
                for user in users_[:random.randint(0, users.count())]:
                    if user not in users_liked:
                        users_disliked.append(user)

                answer.rating.users_liked.add(*users_liked)
                answer.rating.users_disliked.add(*users_disliked)
                answer.rating.like_amount = len(users_liked)
                answer.rating.dislike_amount = len(users_disliked)
                answer.rating.save()
                answer.save()

        answers = QuestionAnswer.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число ответов: {answers.count()}.'))

        return answers

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
                    comment.save()

        comments = AnswerComment.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Число комментариев: {comments.count()}.'))

        return comments


class Command(BaseCommand, Helper):
    help = 'Создание фикстур'

    @transaction.atomic
    def handle(self, *args, **options):
        tags = self.create_tags(tags_amount=15)
        users = self.create_users(users_amount=20)
        questions = self.create_questions(questions_amount=50, users=users, tags=tags)
        answers = self.create_answers(questions=questions, users=users)
        self.create_comments(answers=answers, users=users)
