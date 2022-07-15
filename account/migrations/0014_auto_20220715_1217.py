# Generated by Django 3.2 on 2022-07-15 10:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20220714_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='trade',
            name='expires_in',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 15, 20, 17, 45, 379478, tzinfo=utc)),
        ),
    ]
