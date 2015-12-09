# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20151127_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Symbol',
            field=models.CharField(default=b'N/A', max_length=20),
        ),
    ]
