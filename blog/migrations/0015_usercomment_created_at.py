# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20180804_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 5, 2, 48, 49, 133000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
