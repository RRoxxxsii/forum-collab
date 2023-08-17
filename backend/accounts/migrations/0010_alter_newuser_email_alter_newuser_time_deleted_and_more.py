# Generated by Django 4.2.3 on 2023-08-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_merge_20230817_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Указаный почтовый адрес уже занято.'}, max_length=254, unique=True, verbose_name='Почтовый адрес'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='time_deleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='user_name',
            field=models.CharField(error_messages={'unique': 'Указаное имя уже занято.'}, max_length=150, unique=True, verbose_name='Имя пользователя'),
        ),
    ]
