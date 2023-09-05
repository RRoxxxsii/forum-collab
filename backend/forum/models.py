from accounts.models import NewUser
from django.db import models

from forum.helpers import LikeDislikeModelMixin


class Attachment(models.Model):
    """
    Абстрактный класс для вложений.
    """
    image = models.ImageField(verbose_name='Изображение')
    alt_text = models.CharField(
        verbose_name="Альтернативный текст",
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return str(self.image)


class Rating(models.Model):
    """
    Абстрактный класс для рейтинга.
    """
    like_amount = models.PositiveIntegerField(null=True, default=0)
    dislike_amount = models.PositiveIntegerField(null=True, default=0)

    class Meta:
        abstract = True
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

    def __str__(self):
        return f'Лайки: {self.like_amount}; Дизлайки: {self.dislike_amount}'


class ThemeTag(models.Model):
    """
    Тег (подтема).
    """
    tag_name = models.CharField(max_length=255, verbose_name='Тег', unique=True)
    descriptions = models.TextField(verbose_name='Описание', null=True, blank=True)

    is_relevant = models.BooleanField(default=True, verbose_name='Релеватный тег')
    is_user_tag = models.BooleanField(default=False, verbose_name='Авторский тег')
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True,
                             verbose_name='Автор, если есть', editable=False,
                             related_name='tags')

    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                         editable=False)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Question(models.Model, LikeDislikeModelMixin):
    """
    Вопрос.
    """
    tags = models.ManyToManyField(ThemeTag, verbose_name='Тег', related_name='questions')
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, verbose_name='Автор',
                             related_name='questions', null=True)

    title = models.CharField(max_length=255, verbose_name='Заголовок вопроса')
    content = models.TextField(verbose_name='Вопрос')

    is_solved = models.BooleanField(default=False, verbose_name='Вопрос решен')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def save(self, *args, **kwargs):
        from forum.logic import \
            make_tag_relevant_on_question_save  # Избегаем цикличного импорта

        super(Question, self).save(*args, **kwargs)
        self.rating, _ = QuestionRating.objects.get_or_create(question=self)
        make_tag_relevant_on_question_save(self)


class QuestionImages(Attachment):
    """
    Вложения к вопросу.
    """
    parent = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_images',
                               verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вложение к вопросу'
        verbose_name_plural = 'Вложения к вопросу'


class QuestionRating(Rating):
    """
    Лайки и дизлайки для вопроса. Рейтинг вопроса.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='rating')
    users_liked = models.ManyToManyField(NewUser, related_name='liked_question_ratings', blank=True)
    users_disliked = models.ManyToManyField(NewUser, related_name='disliked_question_ratings', blank=True)

    class Meta:
        verbose_name = 'Рейтинг вопроса'
        verbose_name_plural = 'Рейтинги вопросов'


class QuestionAnswer(models.Model, LikeDislikeModelMixin):
    """
    Ответ на вопрос.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, related_name='question_answers', null=True)

    answer = models.TextField(verbose_name='Текс ответа')

    is_solving = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    def save(self, *args, **kwargs):
        super(QuestionAnswer, self).save(*args, **kwargs)
        self.rating, _ = QuestionAnswerRating.objects.get_or_create(answer=self)


class QuestionAnswerImages(Attachment):
    """
    Вложения к ответу на вопрос.
    """
    parent = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, related_name='answer_images',
                               verbose_name='Ответ')

    class Meta:
        verbose_name = 'Вложение к ответу на вопрос'
        verbose_name_plural = 'Вложения к ответу на вопрос'


class QuestionAnswerRating(Rating):
    """
    Лайки и дизлайки ответа на вопрос. Рейтинг ответа.
    """
    answer = models.OneToOneField(QuestionAnswer, on_delete=models.CASCADE, related_name='rating')
    users_liked = models.ManyToManyField(NewUser, related_name='liked_answer_ratings', blank=True)
    users_disliked = models.ManyToManyField(NewUser, related_name='disliked_answer_ratings', blank=True)

    class Meta:
        verbose_name = 'Рейтинг ответа'
        verbose_name_plural = 'Рейтинги ответов'


class AnswerComment(models.Model):
    """
    Комментарий. Ответ на 'ответ'. Под 'ответ' подразумевается ответ на комментарий.
    """
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, related_name='answer_comments', null=True)
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, related_name='answer_comments',
                                        verbose_name='Ответ на вопрос (ID)')

    comment = models.TextField(max_length=320, verbose_name='Текст комментария')

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
