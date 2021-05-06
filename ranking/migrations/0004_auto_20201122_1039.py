# Generated by Django 3.1.3 on 2020-11-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0003_member_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_posseded', models.BooleanField(default=False, verbose_name='Possédé ?')),
                ('svg', models.TextField(verbose_name='modèle')),
            ],
            options={
                'verbose_name': 'Badges',
                'verbose_name_plural': 'Badges',
            },
        ),
        migrations.RemoveField(
            model_name='member',
            name='badge_old_first',
        ),
        migrations.RemoveField(
            model_name='member',
            name='badge_staff',
        ),
        migrations.RemoveField(
            model_name='member',
            name='badge_streamer',
        ),
        migrations.RemoveField(
            model_name='member',
            name='badge_tournament_winner',
        ),
        migrations.AddField(
            model_name='member',
            name='member_badges',
            field=models.ManyToManyField(to='ranking.Badge', verbose_name='Badges'),
        ),
    ]