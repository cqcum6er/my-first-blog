# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20181101_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Price_1',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Price_30',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Price_7',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2018-11-21'),
        ),
    ]
