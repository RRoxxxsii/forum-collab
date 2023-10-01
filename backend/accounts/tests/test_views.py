import json
import re

from django.core import mail
from django.db.models import Q, Count
from django.urls import reverse

from forum.models import ThemeTag, Question, QuestionAnswer
from forum.tests.test_serializers import generate_photo_file
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import NewUser


class TestRegistrationAPI(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('create-account')

    def test_register_user(self):
        """
        Тестирование регистрации пользователя.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': 'Ax6!a7OpNvq'})
        new_user = NewUser.objects.get(email='a@a.ru')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(new_user)

    def test_user_account_register_without_password(self):
        """
        Регистрация пользователя без указания пароля. Ожидается возбуждение исключения.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        try:
            new_user = NewUser.objects.get(email='a@a.ru')
        except NewUser.DoesNotExist:
            assert True
        else:
            assert False

    def test_user_account_register_with_empty_password(self):
        """
        Регистрация пользователя c пустым паролем.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        try:
            new_user = NewUser.objects.get(email='a@a.ru')
        except NewUser.DoesNotExist:
            assert True
        else:
            assert False

    def test_register_user_simple_password(self):
        """
        Пароль слишком простой, ожидается возбуждение исключения.
        """
        response = self.client.post(self.url, data={'email': 'a@a.ru', 'user_name': 'test-user',
                                                    'password': '12345'})
        self.assertEqual(response.status_code, 400)


class TestEmailConfirmAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('confirm-email-request')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')
        self.user2 = NewUser.objects.create_user(email='testuser2@gmail.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq', email_confirmed=True)

    def test_send_request_user_not_authenticated(self):
        """
        Проверка на возвращение статуса 401 для не аутентифицированого пользователя.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_request_user_authenticated(self):
        """
        Проверка отправки письма пользователю и факта получения.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        email_msg = mail.outbox
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(email_msg), 1)

    def test_email_content(self):
        """
        Проверка содержимого отправленого пользователю письма.
        """
        self.client.force_authenticate(self.user)
        self.client.get(self.url)
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.assertIsNotNone(link)

    def test_email_confirm(self):
        """
        Проверка изменения статуса пользователя email_confirmed.
        """
        self.client.force_authenticate(self.user)
        self.client.get(self.url)
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_confirmed)

    def test_send_request_email_already_confirmed(self):
        """
        Попытка отправить запрос на получение письма, при этом эл. почта у пользователя
        уже подтверждена.
        """
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        email_msg = mail.outbox
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(email_msg), 0)


class TestChangeEmailAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('change-email-confirm')
        self.email_to_change = 'somemail@gmail.com'     # Адрес, на который необходимо изменить
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', email_confirmed=True)

    def test_response_user_not_authenticated(self):
        """
        Тестируем смену почты, когда пользователь не аутентифицирован. Предполагаем код ответа - 401.
        """
        response = self.client.post(self.url, data={'email': 'somemail@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_status_code(self):
        """
        Пользователь аутентифицирован, ожидаемый статус код - 201.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': self.email_to_change})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_response_email_incorrect(self):
        """
        Введеный почтовый адрес некорректен. Ожидаемый статус код - 400.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': 'email-incorrect'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_session_key_exists(self):
        """
        Проверка на то, был ли добавлен почтовый адрес в сессию.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_change})
        self.assertIsNotNone(self.client.session)

    def test_response_email_already_exists(self):
        """
        Попытка указать почтовый адрес, который уже существует для другого пользователя.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': 'testuser@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_content(self):
        """
        Проверка содержимого в письме.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_change})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.assertIsNotNone(link)

    def test_change_email_status_code(self):
        """
        Запрос на получение ссылки на почтовый адрес и переход по ссылке. Статус код - 200.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_change})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_email_result(self):
        """
        Проверка, действительно ли в базе данных изменился email пользователя.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_change})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.client.get(link, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, self.email_to_change)
        self.assertTrue(self.user.email_confirmed)


class TestActiveUserMiddleware(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('change-email-confirm')      # Здесь может быть абсолютно любой url-адрес
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', is_banned=True)

    def test_user_is_banned_but_try_accessing_the_site(self):
        """
        Аутентифицированный и забаненый(is_banned=True) пользователь пытается получить ресурс.
        Должно возбуждаться исключение 403.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={'email': 'somemail@a.ru'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteAccountAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('delete-account')
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq')

    def test_user_is_active_before_delete(self):
        """
        Проверка статуса is_active до того, как отправлен запрос на удаление.
        Ожидаемый результат - is_active is True.
        """
        self.client.force_authenticate(self.user)
        self.assertTrue(self.user.is_active)

    def test_delete_account_response(self):
        """
        Тестирование статус кода ответа. Ожидаемый результат - 200.
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_account_is_active(self):
        """
        Удаление аккаунта. Ожидаемый результат - is_active is False.
        """
        self.client.force_authenticate(self.user)
        self.client.get(self.url)
        self.assertFalse(self.user.is_active)


class TestRestoreAccountAPIView(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('restore-account')
        self.email_to_request = 'testuser@gmail.com'
        self.user = NewUser.objects.create_user(email=self.email_to_request, user_name='testuser',
                                                password='Ax6!a7OpNvq', is_active=False)
        self.user2 = NewUser.objects.create_user(email='emailowned-byanother@user.com', user_name='testuser2',
                                                 password='Ax6!a7OpNvq', is_active=False)

    def test_restore_account_response(self):
        """
        Проверка статуса ответа. Ожидаемый статус - 201.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': self.email_to_request})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_response_email_does_not_exist(self):
        """
        Проверка статуса ответа при некорректно введенном почтовом адресе. Ожидаемый статус - 400.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': 'another-email@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_user_is_active(self):
        """
        Проверка статуса ответа в случае, когда аккаунт пользователя активен
        (нет необходимости восстанавливать). Ожидаемый статус - 400.
        """
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': self.email_to_request})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_when_email_email_is_owned_by_another_user(self):
        """
        Отправка сообщения на почту, которая принадлежит другому пользователю сайта.
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={'email': 'emailowned-byanother@user.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_content(self):
        """
        Проверка, было ли отправлено сообщение на почту.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_request})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.assertIsNotNone(link)

    def test_restore_account_status_code(self):
        """
        Запрос на получение ссылки на почтовый адрес и переход по ссылке. Статус код - 200.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_request})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_account_user_is_active(self):
        """
        Запрос на получение ссылки на почтовый адрес и переход по ссылке. Статус код - 200.
        """
        self.client.force_authenticate(self.user)
        self.client.post(self.url, data={'email': self.email_to_request})
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        self.client.get(link, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


class TestEmailTokenObtainPairView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('token_obtain_pair')
        self.email_to_request = 'testuser@gmail.com'

        self.user = NewUser.objects.create_user(email=self.email_to_request, user_name='testuser',
                                                password='Ax6!a7OpNvq')

    def test_obtain_token(self):
        """
        Получение refresh и access токенов.
        """
        response = self.client.post(self.url, data={'email': self.email_to_request,
                                                    'password': 'Ax6!a7OpNvq'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserViewSet(APITestCase):
    """
    Тестрование ViewSet для пользователя.
    """
    def setUp(self) -> None:
        image = generate_photo_file()
        self.user = NewUser.objects.create_user(email='email@email.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', profile_image=image)

        self.url = reverse('newuser-list')
        self.detail_url = reverse('newuser-detail', kwargs={'pk': self.user.pk})

    def test_list_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_response_status_code(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateProfileImage(APITestCase):

    def setUp(self) -> None:
        self.img_to_update = generate_photo_file()
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', email_confirmed=True)
        self.url = reverse('update-image')

    def test_update_image_status_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data={'profile_image': self.img_to_update})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_image_content(self):
        self.client.force_authenticate(self.user)
        self.client.patch(self.url, data={'profile_image': self.img_to_update})

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_image, self.img_to_update)

    def test_update_profile_img_not_authenticated(self):
        response = self.client.patch(self.url, data={'profile_image': self.img_to_update})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdateProfileAbout(APITestCase):

    def setUp(self) -> None:
        self.img_to_update = generate_photo_file()
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', email_confirmed=True)
        self.url = reverse('update-about')
        self.about = 'Фейковая информация'

    def test_update_about_status_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data={'about': self.about})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_about_content(self):
        self.client.force_authenticate(self.user)
        self.client.patch(self.url, data={'about': self.about})

        self.user.refresh_from_db()
        self.assertEqual(self.user.about, self.about)

    def test_update_profile_about_not_authenticated(self):
        response = self.client.patch(self.url, data={'about': self.about})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetPersonalProfile(APITestCase):

    def setUp(self) -> None:
        img = generate_photo_file()
        self.user = NewUser.objects.create_user(email='testuser@gmail.com', user_name='testuser',
                                                password='Ax6!a7OpNvq', email_confirmed=True,
                                                profile_image=img)
        self.url = reverse('personal-page')

    def test_profile_status_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_status_code_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserRating(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('personal-page')

        for i in range(6):
            user = NewUser.objects.create_user(email=f'testuser{i}@gmail.com', user_name=f'testuser{i}',
                                               password='Ax6!a7OpNvq', email_confirmed=True)
        for i in range(30):
            self.tag = ThemeTag.objects.create(tag_name=f'django{i}')

        tags = ThemeTag.objects.all()
        users = NewUser.objects.all()
        self.user3 = users[3]
        self.user2 = users[2]

        self.question1 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question1.tags.add(tags[0], tags[1], tags[2], tags[3])

        self.question2 = Question.objects.create(title='Заголовок', content='Контент', user=users[1], is_solved=True)
        self.question2.tags.add(tags[5], tags[6], tags[2], tags[8])

        self.question3 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question3.tags.add(tags[9], tags[10], tags[2], tags[12])

        self.question4 = Question.objects.create(title='Заголовок', content='Контент', user=users[1])
        self.question4.tags.add(tags[2], tags[3], tags[5], tags[16])

        self.question5 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question5.tags.add(tags[17], tags[18])

        self.question6 = Question.objects.create(title='Заголовок', content='Контент', user=users[1], is_solved=True)
        self.question6.tags.add(tags[3])

        self.question7 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question7.tags.add(tags[4], tags[18], tags[2])

        self.question8 = Question.objects.create(title='Заголовок', content='Контент', user=users[0])
        self.question8.tags.add(tags[25], tags[17], tags[6])

        self.question9 = Question.objects.create(title='Заголовок', content='Контент', user=users[0])
        self.question9.tags.add(tags[2], tags[4], tags[24], tags[3])

        self.question10 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question10.tags.add(tags[23])

        self.question11 = Question.objects.create(title='Заголовок', content='Контент', user=users[0], is_solved=True)
        self.question11.tags.add(tags[14])

        self.answer1 = QuestionAnswer.objects.create(question=self.question1, user=users[3], answer='AAA',
                                                     is_solving=True)
        self.answer2 = QuestionAnswer.objects.create(question=self.question1, user=users[4], answer='AAA')
        self.answer3 = QuestionAnswer.objects.create(question=self.question1, user=users[5], answer='AAA')

        self.answer4 = QuestionAnswer.objects.create(question=self.question2, user=users[3], answer='AAA',
                                                     is_solving=True)
        self.answer5 = QuestionAnswer.objects.create(question=self.question2, user=users[4], answer='AAA')
        self.answer6 = QuestionAnswer.objects.create(question=self.question2, user=users[5], answer='AAA')

        self.answer7 = QuestionAnswer.objects.create(question=self.question3, user=users[3], answer='AAA')
        self.answer8 = QuestionAnswer.objects.create(question=self.question3, user=users[4], answer='AAA',
                                                     is_solving=True)
        self.answer9 = QuestionAnswer.objects.create(question=self.question3, user=users[5], answer='AAA')

        self.answer10 = QuestionAnswer.objects.create(question=self.question4, user=users[3], answer='AAA')
        self.answer11 = QuestionAnswer.objects.create(question=self.question4, user=users[4], answer='AAA')
        self.answer12 = QuestionAnswer.objects.create(question=self.question4, user=users[5], answer='AAA')

        self.answer10 = QuestionAnswer.objects.create(question=self.question5, user=users[3], answer='AAA',
                                                      is_solving=True)
        self.answer11 = QuestionAnswer.objects.create(question=self.question5, user=users[4], answer='AAA')
        self.answer12 = QuestionAnswer.objects.create(question=self.question5, user=users[5], answer='AAA')

        self.answer13 = QuestionAnswer.objects.create(question=self.question6, user=users[3], answer='AAA',
                                                      is_solving=True)

        self.answer14 = QuestionAnswer.objects.create(question=self.question7, user=users[3], answer='AAA',
                                                      is_solving=True)
        self.answer15 = QuestionAnswer.objects.create(question=self.question7, user=users[4], answer='AAA')
        self.answer16 = QuestionAnswer.objects.create(question=self.question7, user=users[5], answer='AAA')

        for i in range(10):
            QuestionAnswer.objects.create(question=self.question11, user=users[2], answer='AAA', is_solving=True)

    def test_answer_get_rating_user3(self):
        self.client.force_authenticate(self.user3)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        user_answered_question_tags = ThemeTag.objects.filter(
            questions__question_answers__user_id=self.user3.id
        ).distinct()

        self.assertEqual(len(user_answered_question_tags), 14)
        self.assertEqual(content.get('amount_solved'), 5)

    def test_answer_get_rating_user2(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        content = json.loads(response.content.decode())
        user_answered_question_tags = ThemeTag.objects.filter(
            questions__question_answers__user_id=self.user2.id
        ).distinct()

        self.assertEqual(len(user_answered_question_tags), 1)
        self.assertEqual(content.get('amount_solved'), 10)
