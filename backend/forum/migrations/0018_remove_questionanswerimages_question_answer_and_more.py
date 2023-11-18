# Generated by Django 4.2.3 on 2023-08-25 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_remove_questionanswerimages_question_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswerimages',
            name='question_answer',
        ),
        migrations.RemoveField(
            model_name='questionimages',
            name='question',
        ),
        migrations.AddField(
            model_name='questionanswerimages',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_images', to='forum.questionanswer', verbose_name='Ответ'),
        ),
        migrations.AddField(
            model_name='questionimages',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_images', to='forum.question', verbose_name='Вопрос'),
        ),
    ]