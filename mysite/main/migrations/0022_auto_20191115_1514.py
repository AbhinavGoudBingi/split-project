# Generated by Django 2.2.6 on 2019-11-15 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20191115_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.FileField(default='default.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 15, 15, 14, 55, 542724), verbose_name='date published'),
        ),
    ]
