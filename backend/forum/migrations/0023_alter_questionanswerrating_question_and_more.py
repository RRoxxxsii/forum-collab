# Generated by Django 4.2.3 on 2023-08-26 03:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0022_remove_answercomment_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswerrating',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer_rating', to='forum.questionanswer'),
        ),
        migrations.AlterField(
            model_name='questionrating',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_rating', to='forum.question'),
        ),
    ]
