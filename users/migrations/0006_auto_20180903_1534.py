# Generated by Django 2.1.1 on 2018-09-03 15:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180903_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='custom_groups',
            field=models.ManyToManyField(blank=True, to='main.CustomGroup'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friend_requests_received',
            field=models.ManyToManyField(blank=True, related_name='_customuser_friend_requests_received_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friend_requests_sent',
            field=models.ManyToManyField(blank=True, related_name='_customuser_friend_requests_sent_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_customuser_friends_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='posts_to_show',
            field=models.ManyToManyField(blank=True, to='main.Post'),
        ),
    ]
