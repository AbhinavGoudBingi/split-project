# Generated by Django 2.2.6 on 2019-11-15 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20191115_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 15, 11, 15, 44, 39908), verbose_name='date published'),
        ),
    ]
