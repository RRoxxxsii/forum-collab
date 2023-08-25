from accounts.models import NewUser
from django.db import models


class ThemeTag(models.Model):
    """
    Тег (подтема).
    """
    tag = models.CharField(max_length=255, verbose_name='Тег', unique=True)
    descriptions = models.TextField(verbose_name='Описание', null=True, blank=True)

    is_relevant = models.BooleanField(default=True, verbose_name='Релеватный тег')
    is_user_tag = models.BooleanField(default=False, verbose_name='Авторский тег')
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True,
                             verbose_name='Автор, если есть', editable=False,
                             related_name='tags')

    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                         editable=False)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Question(models.Model):
    """
    Вопрос.
    """
    tags = models.ManyToManyField(ThemeTag, verbose_name='Тег', related_name='questions')
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, verbose_name='Автор',
                             related_name='questions', null=True)

    title = models.CharField(max_length=255, verbose_name='Заголовок вопроса')
    content = models.TextField(verbose_name='Вопрос')

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
        make_tag_relevant_on_question_save(self)


class QuestionImages(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_images')
    image = models.ImageField(verbose_name='Изображение', upload_to='question_img/%Y/%m/%d/')
    alt_text = models.CharField(
        verbose_name="Альтернативый текст",
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Вложение к вопросу'
        verbose_name_plural = 'Вложения к вопросу'

    def __str__(self):
        return str(self.image)


class QuestionRating(models.Model):
    """
    Лайки и дизлайки для вопроса. Рейтинг вопроса.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    like_amount = models.PositiveIntegerField(null=True)
    dislike_amount = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'Лайки: {self.like_amount}; Дизлайки: {self.dislike_amount}'

    class Meta:
        verbose_name = 'Рейтинг вопроса'
        verbose_name_plural = 'Рейтинги вопросов'


class QuestionAnswer(models.Model):
    """
    Ответ на вопрос.
    """
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, related_name='question_answers', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')

    answer = models.TextField(verbose_name='Текс ответа', max_length=320)

    is_solving = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'


class QuestionAnswerImages(models.Model):
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, related_name='answer_images')
    image = models.ImageField(verbose_name='Изображение', upload_to='answer_img/%Y/%m/%d/')
    alt_text = models.CharField(
        verbose_name="Альтернативый текст",
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Вложение к ответу на вопрос'
        verbose_name_plural = 'Вложения к ответу на вопрос'


class QuestionAnswerRating(models.Model):
    """
    Лайки и дизлайки ответа на вопрос. Рейтинг ответа.
    """
    question = models.OneToOneField(QuestionAnswer, on_delete=models.CASCADE)
    like_amount = models.PositiveIntegerField(null=True)
    dislike_amount = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'Лайки: {self.like_amount}; Дизлайки: {self.dislike_amount}'

    class Meta:
        verbose_name = 'Рейтинг ответа'
        verbose_name_plural = 'Рейтинги ответов'


class AnswerComment(models.Model):
    """
    Комментарий. Ответ на 'ответ'. Под 'ответ' подразумевается ответ на комментарий.
    """
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, related_name='answer_comments', null=True)
    comment = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, related_name='answer_comments')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
