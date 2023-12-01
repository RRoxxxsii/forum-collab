
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
            name='AnswerComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=320, verbose_name='Текст комментария')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.answercomment')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарий',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок вопроса')),
                ('content', models.TextField(verbose_name='Вопрос')),
                ('is_solved', models.BooleanField(default=False, verbose_name='Вопрос решен')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
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
                ('answer', models.TextField(verbose_name='Текс ответа')),
                ('is_solving', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='forum.question')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответ на вопрос',
                'verbose_name_plural': 'Ответы на вопросы',
            },
        ),
        migrations.CreateModel(
            name='ThemeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255, unique=True, verbose_name='Тег')),
                ('descriptions', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('is_relevant', models.BooleanField(default=True, verbose_name='Релевантный тег')),
                ('is_user_tag', models.BooleanField(default=False, verbose_name='Авторский тег')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to=settings.AUTH_USER_MODEL, verbose_name='Автор, если есть')),
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
                ('like_amount', models.PositiveIntegerField(default=0, null=True)),
                ('dislike_amount', models.PositiveIntegerField(default=0, null=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='forum.question')),
                ('users_complained', models.ManyToManyField(blank=True, related_name='question_rating_complained', to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи')),
                ('users_disliked', models.ManyToManyField(blank=True, related_name='disliked_question_ratings', to=settings.AUTH_USER_MODEL)),
                ('users_liked', models.ManyToManyField(blank=True, related_name='liked_question_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рейтинг вопроса',
                'verbose_name_plural': 'Рейтинги вопросов',
            },
        ),
        migrations.CreateModel(
            name='QuestionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альтернативный текст')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_images', to='forum.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вложение к вопросу',
                'verbose_name_plural': 'Вложения к вопросу',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_amount', models.PositiveIntegerField(default=0, null=True)),
                ('dislike_amount', models.PositiveIntegerField(default=0, null=True)),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='forum.questionanswer')),
                ('users_complained', models.ManyToManyField(blank=True, related_name='answer_rating_complained', to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи')),
                ('users_disliked', models.ManyToManyField(blank=True, related_name='disliked_answer_ratings', to=settings.AUTH_USER_MODEL)),
                ('users_liked', models.ManyToManyField(blank=True, related_name='liked_answer_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рейтинг ответа',
                'verbose_name_plural': 'Рейтинги ответов',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswerImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Альтернативный текст')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_images', to='forum.questionanswer', verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Вложение к ответу на вопрос',
                'verbose_name_plural': 'Вложения к ответу на вопрос',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', to='forum.themetag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.CreateModel(
            name='CommentRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='forum.answercomment')),
                ('users_complained', models.ManyToManyField(blank=True, related_name='comment_rating_complained', to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи')),
            ],
            options={
                'verbose_name': 'Рейтинг комментария',
                'verbose_name_plural': 'Рейтинги комментариев',
            },
        ),
        migrations.AddField(
            model_name='answercomment',
            name='question_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_comments', to='forum.questionanswer', verbose_name='Ответ на вопрос (ID)'),
        ),
        migrations.AddField(
            model_name='answercomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
