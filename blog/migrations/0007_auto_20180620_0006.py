# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_all_ks_join_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_ks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Day', models.DateField(default=b'2018-06-20')),
                ('Symbol', models.CharField(default=b'N/A', max_length=20)),
                ('LastPrice', models.CharField(default=b'N/A', max_length=30)),
                ('FiftyTwoWkChg', models.CharField(default=b'N/A', max_length=30)),
                ('FiftyTwoWkHi', models.CharField(default=b'N/A', max_length=30)),
                ('FiftyTwoWkLo', models.CharField(default=b'N/A', max_length=30)),
                ('DivYild', models.CharField(default=b'N/A', max_length=30)),
                ('TrailPE', models.CharField(default=b'N/A', max_length=30)),
                ('ForwardPE', models.CharField(default=b'N/A', max_length=30)),
                ('PEG_Ratio', models.CharField(default=b'N/A', max_length=30)),
                ('PpS', models.CharField(default=b'N/A', max_length=30)),
                ('PpB', models.CharField(default=b'N/A', max_length=30)),
                ('Market_Cap', models.CharField(default=b'N/A', max_length=30)),
                ('Free_Cash_Flow', models.CharField(default=b'N/A', max_length=30)),
                ('Market_per_CashFlow', models.CharField(default=b'N/A', max_length=30)),
                ('Enterprise_per_EBITDA', models.CharField(default=b'N/A', max_length=30)),
                ('Name', models.CharField(default=b'N/A', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2018-06-20'),
        ),
    ]
