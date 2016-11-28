# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_post_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2016-11-27'),
        ),
    ]
