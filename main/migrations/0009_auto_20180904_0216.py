# Generated by Django 2.1.1 on 2018-09-04 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180904_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='groups_owned', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]