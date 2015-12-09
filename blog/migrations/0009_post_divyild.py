# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20151205_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='DivYild',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
