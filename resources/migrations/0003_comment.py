# Generated by Django 4.2.2 on 2023-07-21 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0002_alter_article_options_alter_article_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='resources.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'indexes': [models.Index(fields=['created'], name='resources_c_created_cc84b9_idx')],
            },
        ),
    ]
