# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-15 22:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_auto_20190315_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_ks',
            name='DivYild_v0',
        ),
    ]
