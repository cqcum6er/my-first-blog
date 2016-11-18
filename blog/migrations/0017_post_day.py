# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Day',
            field=models.CharField(default=b'N/A', max_length=20),
        ),
    ]
