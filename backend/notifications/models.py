from accounts.models import NewUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class NotificationManager(models.query.QuerySet):
    """
    Реализует QuerySet для уведомлений.
    """

    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=False)

    def mark_all_as_read(self):
        queryset = self.unread()
        queryset.update(unread=False)

    def mark_all_as_unread(self):
        queryset = self.read()
        queryset.update(unread=True)


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

    sender = models.ForeignKey(
        NewUser,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Отправитель'
    )
    receiver = models.ForeignKey(
        NewUser,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        related_name='notifications'
    )

    level = models.CharField('Цель уведомления', choices=LEVEL_CHOICES, default=INFO)

    # Целевой объект, автор которого получит уведомление, т.е. относится к receiver
    target = GenericForeignKey('target_content_type', 'target_object_id')
    target_object_id = models.PositiveIntegerField('ID целевого объекта получателя')
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='target_action_objects',
        verbose_name='Тип объекта получателя'
    )

    # Текущий объект, который был создан, относится к sender
    action_obj = GenericForeignKey('action_obj_content_type', 'action_obj_object_id')
    action_obj_object_id = models.PositiveIntegerField(
        'ID объекта отправителя',
        blank=True,
        null=True
    )
    action_obj_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='action_obj_action_objects',
        verbose_name='Тип объекта отправителя',
        blank=True,
        null=True
    )

    text = models.TextField('Текст уведомления', null=True, blank=True)
    emailed = models.BooleanField('Отправлять уведомления', default=False)
    unread = models.BooleanField('Не прочитано', default=True)
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)

    objects = NotificationManager.as_manager()

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-creation_date',)
        abstract = False

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
