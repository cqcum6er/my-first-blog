# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_forwardpe'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='PEG_Ratio',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='post',
            name='PpS',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
