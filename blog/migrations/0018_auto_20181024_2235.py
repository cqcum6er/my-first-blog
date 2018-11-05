# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20180804_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_ks_DatePriceDiff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Day', models.DateField(default=b'2018-10-24')),
                ('Name', models.CharField(default=b'N/A', max_length=50)),
                ('Symbol', models.CharField(default=b'N/A', max_length=20)),
                ('Price_1', models.CharField(default=b'N/A', max_length=30)),
                ('Price_7', models.CharField(default=b'N/A', max_length=30)),
                ('Price_30', models.CharField(default=b'N/A', max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2018-10-24'),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='message',
            field=models.TextField(max_length=2000),
        ),
    ]
