# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_post_enterprise_per_ebitda'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Name',
            field=models.CharField(default=b'N/A', max_length=50),
        ),
    ]
