# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0002_p4user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ldap_user', models.ForeignKey(to='projectaccess.LDAPUser')),
                ('p4_user', models.ForeignKey(to='projectaccess.P4User')),
            ],
        ),
    ]
