# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-16 01:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_auto_20190315_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='all_ks',
            old_name='TrailPE_v1',
            new_name='TrailPE',
        ),
    ]
