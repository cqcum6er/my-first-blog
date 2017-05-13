# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20161127_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=80)),
                ('contact_email', models.EmailField(max_length=254)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2017-05-13'),
        ),
    ]
