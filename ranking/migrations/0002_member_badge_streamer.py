# Generated by Django 3.1.3 on 2020-11-22 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='badge_streamer',
            field=models.BooleanField(default=False, verbose_name='Streamer'),
        ),
    ]
