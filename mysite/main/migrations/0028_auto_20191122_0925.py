# Generated by Django 2.2.6 on 2019-11-22 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20191122_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 9, 25, 58, 483699), verbose_name='date published'),
        ),
    ]
