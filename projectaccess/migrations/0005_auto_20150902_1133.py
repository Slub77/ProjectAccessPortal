# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0004_auto_20150901_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metauser',
            name='ldap_user',
            field=models.OneToOneField(null=True, to='projectaccess.LDAPUser'),
        ),
        migrations.AlterField(
            model_name='metauser',
            name='p4_user',
            field=models.OneToOneField(null=True, to='projectaccess.P4User'),
        ),
    ]
