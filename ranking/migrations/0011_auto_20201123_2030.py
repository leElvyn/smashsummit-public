# Generated by Django 3.1.3 on 2020-11-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0010_member_is_winning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_winning',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
