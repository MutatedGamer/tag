# Generated by Django 2.1.1 on 2018-09-02 00:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroup',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customgroup',
            name='posts',
            field=models.ManyToManyField(to='main.Post'),
        ),
    ]
