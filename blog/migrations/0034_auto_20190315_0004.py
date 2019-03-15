# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-15 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_auto_20190314_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='all_ks',
            old_name='FiftyTwoWkChg',
            new_name='FiftyTwoWkChg_v0',
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(db_index=True, default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='all_ks_datepricediff',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2019-03-15'),
        ),
    ]
