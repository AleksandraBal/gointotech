# Generated by Django 4.2.2 on 2023-07-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_alter_article_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=2000),
        ),
    ]
