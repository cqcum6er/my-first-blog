# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20180730_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 2, 7, 5, 47, 157000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='all_ks',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='all_ks_join',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='all_ks_join_unique',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='index_dj',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='index_sp500',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='nasdaq_post',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='sp500_post',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
        migrations.AlterField(
            model_name='sp500_post_sorted',
            name='Day',
            field=models.DateField(default=b'2018-08-02'),
        ),
    ]
