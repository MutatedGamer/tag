# Generated by Django 2.1.1 on 2018-09-08 14:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='members',
            field=models.ManyToManyField(related_name='groups_in', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customgroup',
            name='posts',
            field=models.ManyToManyField(to='main.Post'),
        ),
        migrations.AlterField(
            model_name='customgroup',
            name='to_approve',
            field=models.ManyToManyField(related_name='posts_to_approve', to='main.Post'),
        ),
    ]
