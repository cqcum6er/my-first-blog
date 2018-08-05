# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20180804_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercomment',
            name='Day',
        ),
        migrations.AddField(
            model_name='usercomment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
    ]
