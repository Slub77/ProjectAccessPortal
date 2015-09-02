# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0006_auto_20150902_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='p4group',
            old_name='member_groups',
            new_name='member_subgroups',
        ),
    ]
