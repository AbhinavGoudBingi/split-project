# Generated by Django 2.2.6 on 2019-11-15 06:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20191115_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 15, 6, 43, 40, 71388), verbose_name='date published'),
        ),
    ]
