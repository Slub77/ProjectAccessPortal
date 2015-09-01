# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0003_metauser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metauser',
            name='ldap_user',
            field=models.ForeignKey(to='projectaccess.LDAPUser', null=True),
        ),
        migrations.AlterField(
            model_name='metauser',
            name='p4_user',
            field=models.ForeignKey(to='projectaccess.P4User', null=True),
        ),
    ]
