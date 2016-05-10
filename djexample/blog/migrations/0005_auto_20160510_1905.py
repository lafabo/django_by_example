# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160510_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default=datetime.datetime(2016, 5, 10, 19, 5, 52, 722461, tzinfo=utc), max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 19, 5, 30, 235289, tzinfo=utc)),
        ),
    ]
