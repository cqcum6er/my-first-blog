# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_trailpe'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ForwardPE',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
