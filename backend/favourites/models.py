from django.db import models

from accounts.models import NewUser
from forum.models import Question


class Favourite(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='ID вопроса')
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, verbose_name='Автор')
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return self.question
