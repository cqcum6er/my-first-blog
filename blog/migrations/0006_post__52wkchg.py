# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_lastprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='_52WkChg',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
