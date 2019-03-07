# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20181224_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(default=b'2019-02-08', db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='DivYild',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Enterprise_per_EBITDA',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='FiftyTwoWkChg',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='FiftyTwoWkHi',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='FiftyTwoWkLo',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='ForwardPE',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Free_Cash_Flow',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='LastPrice',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Market_Cap',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Market_per_CashFlow',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Name',
            field=models.CharField(default=b'N/A', max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='PEG_Ratio',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='PpB',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='PpS',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Sector',
            field=models.CharField(default=b'N/A', max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Symbol',
            field=models.CharField(default=b'N/A', max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='TrailPE',
            field=models.CharField(default=b'N/A', max_length=30, db_index=True),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2019-02-08'),
        ),
    ]
