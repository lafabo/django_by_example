# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique_for_date='published', max_length=250)),
                ('body', models.TextField()),
                ('publish', models.DateTimeField(default=datetime.datetime(2016, 5, 8, 13, 17, 23, 293789, tzinfo=utc))),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='draft', choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='blog_posts')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
