# Generated by Django 4.2.2 on 2023-08-19 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_alter_article_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
