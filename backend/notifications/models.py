from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import NewUser


class Notification(models.Model):

    """
    Класс пользовательских уведомлений.

    <sender> - поле, указывающее пользователя, который сделал действие,
    'отправляющее' уведомление.
    <receiver> - поле, указывающее пользователя-получателя.
    <level> - тип уведомления: сообщение об успехе, оповещение,
    предупреждение, неудача.
    <action_obj> - объект, созданный <sender>, т.е. объект - инициатор
    уведомления, дочерний объект.
    <target> - целевой объект, автор которого получает уведомление, является
    'родительским' для <action_obj>. <target> - Question; <action_obj> - Answer.
    """

    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    FAIL = 'fail'

    LEVEL_CHOICES = [
        (SUCCESS, 'success'),
        (INFO, 'info'),
        (WARNING, 'warning'),
        (FAIL, 'fail')
    ]

    sender = models.ForeignKey(NewUser,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               verbose_name='Отправитель',
                               related_name='sender_notifications')
    receiver = models.ForeignKey(NewUser,
                                 on_delete=models.CASCADE,
                                 verbose_name='Получатель',
                                 related_name='receiver_notifications')

    level = models.CharField(verbose_name='Цель уведомления', choices=LEVEL_CHOICES, default=INFO)

    # Целевой объект, автор которого получит уведомление, т.е. относится к receiver
    target = GenericForeignKey('target_content_type', 'target_object_id')
    target_object_id = models.PositiveIntegerField(verbose_name='ID целевого объекта получателя')
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='target_action_objects',
        verbose_name='Тип объекта получателя'
    )

    # Текущий объект, который был создан, относится к sender
    action_obj = GenericForeignKey('action_obj_content_type', 'action_obj_object_id')
    action_obj_object_id = models.PositiveIntegerField(verbose_name='ID объекта отправителя',
                                                       blank=True, null=True)
    action_obj_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='action_obj_action_objects',
        verbose_name='Тип объекта отправителя',
        blank=True,
        null=True
    )

    text = models.TextField(verbose_name='Текст уведомления', null=True, blank=True)
    emailed = models.BooleanField(default=False, verbose_name='Отправлять уведомления')
    unread = models.BooleanField(default=True, verbose_name='Не прочитано')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-creation_date',)
        abstract = False

    def __str__(self):
        return self.text

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
