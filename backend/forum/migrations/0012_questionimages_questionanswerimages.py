# Generated by Django 4.2.3 on 2023-08-24 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_rename_author_question_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альтернативый текст')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_images', to='forum.question')),
            ],
            options={
                'verbose_name': 'Вложение к вопросу',
                'verbose_name_plural': 'Вложения к вопросу',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альтернативый текст')),
                ('question_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_images', to='forum.question')),
            ],
            options={
                'verbose_name': 'Вложение к ответу на вопрос',
                'verbose_name_plural': 'Вложения к ответу на вопрос',
            },
        ),
    ]