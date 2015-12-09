# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_divyild'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='TrailPE',
            field=models.CharField(default=b'N/A', max_length=30),
        ),
    ]
