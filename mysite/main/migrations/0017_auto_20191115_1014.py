# Generated by Django 2.2.6 on 2019-11-15 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20191115_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 15, 10, 14, 15, 148229), verbose_name='date published'),
        ),
    ]
