# Generated by Django 3.2 on 2022-06-24 21:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220624_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fax',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='firstname',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='home',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idback',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idcardtype',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idfront',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idnumber',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastname',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilepix',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='trade',
            name='expires_in',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 7, 11, 28, 582031, tzinfo=utc)),
        ),
    ]