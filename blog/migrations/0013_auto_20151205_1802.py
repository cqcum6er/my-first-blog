# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20151205_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Market_Cap',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='post',
            name='PpB',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
