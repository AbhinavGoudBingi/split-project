# Generated by Django 2.2.6 on 2019-11-22 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20191122_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 11, 7, 52, 658516), verbose_name='date published'),
        ),
    ]
