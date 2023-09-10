# Generated by Django 4.2.2 on 2023-08-06 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_alter_mailthread_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mail.mailthread'),
        ),
    ]