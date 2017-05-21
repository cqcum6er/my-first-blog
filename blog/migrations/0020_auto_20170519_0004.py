# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20170513_1219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercomment',
            old_name='contact_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='usercomment',
            old_name='content',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='usercomment',
            old_name='contact_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='post',
            name='Day',
            field=models.DateField(default=b'2017-05-19'),
        ),
    ]
