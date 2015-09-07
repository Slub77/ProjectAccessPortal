# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0012_paproject_p4_access_group_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paproject',
            name='users_with_access',
        ),
        migrations.AddField(
            model_name='pauserprojectaccess',
            name='project',
            field=models.ForeignKey(default=None, to='projectaccess.PAProject'),
            preserve_default=False,
        ),
    ]
