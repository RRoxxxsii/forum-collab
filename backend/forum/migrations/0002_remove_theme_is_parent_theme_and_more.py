# Generated by Django 4.2.3 on 2023-08-15 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='is_parent_theme',
        ),
        migrations.RemoveField(
            model_name='theme',
            name='parent_theme',
        ),
    ]
