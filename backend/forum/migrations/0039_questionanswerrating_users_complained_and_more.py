# Generated by Django 4.2.3 on 2023-10-11 06:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0038_remove_questionanswer_parent_answercomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswerrating',
            name='users_complained',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи'),
        ),
        migrations.AddField(
            model_name='questionrating',
            name='users_complained',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи'),
        ),
        migrations.CreateModel(
            name='CommentRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='forum.answercomment')),
                ('users_complained', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пожаловавшиеся пользователи')),
            ],
        ),
    ]
