# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20151205_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Free_Cash_Flow',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
        migrations.AddField(
            model_name='post',
            name='Market_per_CashFlow',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
