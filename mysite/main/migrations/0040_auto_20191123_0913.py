# Generated by Django 2.2.6 on 2019-11-23 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20191123_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendt',
            name='time',
            field=models.DateField(default=datetime.datetime(2019, 11, 23, 9, 13, 9, 73776)),
        ),
    ]
