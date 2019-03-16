# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-15 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_remove_all_ks_lastprice_v0'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_ks',
            name='FiftyTwoWkChg_v1',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(db_index=True, default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2019-03-14'),
        ),
    ]