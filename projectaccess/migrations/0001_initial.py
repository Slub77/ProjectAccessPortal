# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LDAPUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dn', models.CharField(max_length=1024, verbose_name=b'Distinguished Name')),
                ('uid', models.CharField(max_length=256, verbose_name=b'User ID')),
                ('cn', models.CharField(max_length=1024, verbose_name=b'Canonical Name')),
                ('mail', models.CharField(max_length=1024, verbose_name=b'E-Mail')),
            ],
        ),
    ]
