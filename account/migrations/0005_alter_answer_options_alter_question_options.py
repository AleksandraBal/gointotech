# Generated by Django 4.2.2 on 2023-07-04 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_answer_respondent_question_respondent_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('-posted',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-posted',)},
        ),
    ]
