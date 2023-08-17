# Generated by Django 4.2.3 on 2023-08-15 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок вопроса')),
                ('content', models.TextField(verbose_name='Вопрос')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(default='Неизвестный автор', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tags', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=320, verbose_name='Текс ответа')),
                ('is_solving', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='forum.question')),
                ('user', models.ForeignKey(default='Гость', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='question_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответ на вопрос',
                'verbose_name_plural': 'Ответы на вопросы',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255, unique=True, verbose_name='Подтема / Тег')),
                ('descriptions', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('is_parent_theme', models.BooleanField(default=False)),
                ('parent_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tags', to='forum.theme', verbose_name='Родительская тема')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='QuestionRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_amount', models.PositiveIntegerField(null=True)),
                ('dislike_amount', models.PositiveIntegerField(null=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forum.question')),
            ],
            options={
                'verbose_name': 'Рейтинг вопроса',
                'verbose_name_plural': 'Рейтинги вопросов',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_amount', models.PositiveIntegerField(null=True)),
                ('dislike_amount', models.PositiveIntegerField(null=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forum.questionanswer')),
            ],
            options={
                'verbose_name': 'Рейтинг ответа',
                'verbose_name_plural': 'Рейтинги ответов',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_tags', to='forum.theme', verbose_name='Тег'),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_comments', to='forum.questionanswer')),
                ('user', models.ForeignKey(default='Гость', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='answer_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарий',
            },
        ),
    ]