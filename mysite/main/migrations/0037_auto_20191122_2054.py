# Generated by Django 2.2.6 on 2019-11-22 20:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20191122_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendt',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 20, 54, 53, 579011, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 20, 54, 53, 577487), verbose_name='date published'),
        ),
    ]
