# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0009_auto_20150902_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.CharField(max_length=128, verbose_name=b'Block')),
                ('name', models.CharField(max_length=1024, verbose_name=b'Name')),
                ('members', models.ManyToManyField(to='projectaccess.MetaUser')),
                ('p4_group', models.OneToOneField(null=True, to='projectaccess.P4Group')),
            ],
        ),
    ]
