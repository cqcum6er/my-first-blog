# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post__52wkchg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='_52WkChg',
            new_name='FiftyTwoWkChg',
        ),
    ]
