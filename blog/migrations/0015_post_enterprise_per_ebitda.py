# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20151205_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Enterprise_per_EBITDA',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
