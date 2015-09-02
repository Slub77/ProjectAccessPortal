# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0007_auto_20150902_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='p4group',
            old_name='group',
            new_name='name',
        ),
    ]
