# Generated by Django 2.1.1 on 2018-09-13 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_notification_for_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='for_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_to', to='main.Post'),
        ),
    ]