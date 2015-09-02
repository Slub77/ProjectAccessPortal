# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0008_auto_20150902_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metaproject',
            name='members',
        ),
        migrations.RemoveField(
            model_name='metaproject',
            name='p4_group',
        ),
        migrations.DeleteModel(
            name='MetaProject',
        ),
    ]
