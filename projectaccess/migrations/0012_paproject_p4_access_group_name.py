# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0011_auto_20150904_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='paproject',
            name='p4_access_group_name',
            field=models.CharField(default='', max_length=1024, verbose_name=b'P4AccessGroupName'),
            preserve_default=False,
        ),
    ]
