# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-15 23:31
from __future__ import unicode_literals

from django.db import migrations

def populate_new_col(apps, schema_editor):
    all_ks = apps.get_model('blog', 'all_ks')
    for ks in all_ks.objects.all():
        print ks.Day, ks.Symbol, ks.TrailPE
        try:
            ks.TrailPE_v1 = float(ks.TrailPE)
        except ValueError:
            ks.TrailPE_v1 = None
        ks.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0042_all_ks_trailpe_v1'),
    ]

    operations = [
        migrations.RunPython(populate_new_col),
    ]