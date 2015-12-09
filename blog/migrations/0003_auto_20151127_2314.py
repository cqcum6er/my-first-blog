# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151126_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Symbol',
            field=models.CharField(default=b'N/A', unique=True, max_length=20),
        ),
    ]
