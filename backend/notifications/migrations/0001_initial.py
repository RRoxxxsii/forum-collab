# Generated by Django 4.2.3 on 2023-11-24 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('fail', 'fail')], default='info', verbose_name='Цель уведомления')),
                ('target_object_id', models.PositiveIntegerField(verbose_name='ID целевого объекта получателя')),
                ('action_obj_object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='ID объекта отправителя')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст уведомления')),
                ('emailed', models.BooleanField(default=False, verbose_name='Отправлять уведомления')),
                ('unread', models.BooleanField(default=True, verbose_name='Не прочитано')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('action_obj_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_obj_action_objects', to='contenttypes.contenttype', verbose_name='Тип объекта отправителя')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('target_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_action_objects', to='contenttypes.contenttype', verbose_name='Тип объекта получателя')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ('-creation_date',),
                'abstract': False,
            },
        ),
    ]
