# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-08 21:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20190308_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_ks',
            name='LastPrice_v0',
        ),
    ]
