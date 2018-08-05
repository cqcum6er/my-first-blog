# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_usercomment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercomment',
            name='created_at',
        ),
        migrations.AddField(
            model_name='usercomment',
            name='Day',
            field=models.DateField(default=b'2018-08-04'),
        ),
    ]
