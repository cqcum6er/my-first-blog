# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_all_ks_join'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='sp500_post_NoID_sorted',
            new_name='sp500_post_sorted',
        ),
    ]
