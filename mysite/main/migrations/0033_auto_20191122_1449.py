# Generated by Django 2.2.6 on 2019-11-22 14:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20191122_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendt',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 14, 49, 18, 894800, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 14, 49, 18, 893318), verbose_name='date published'),
        ),
    ]