# Generated by Django 2.2.6 on 2019-11-22 20:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20191122_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendt',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 20, 46, 27, 860009, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 20, 46, 27, 858430), verbose_name='date published'),
        ),
    ]
