# Generated by Django 2.2.6 on 2019-11-22 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20191122_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendt',
            name='tag',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 11, 15, 1, 983618), verbose_name='date published'),
        ),
    ]
