# Generated by Django 4.2.3 on 2023-09-07 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0035_answercomment_updated_question_updated_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answercomment',
            old_name='updated',
            new_name='updated_date',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='updated',
            new_name='updated_date',
        ),
        migrations.RenameField(
            model_name='questionanswer',
            old_name='updated',
            new_name='updated_date',
        ),
    ]
