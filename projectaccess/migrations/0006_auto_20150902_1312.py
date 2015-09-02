# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0005_auto_20150902_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('members', models.ManyToManyField(to='projectaccess.MetaUser')),
            ],
        ),
        migrations.CreateModel(
            name='P4Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=1024, verbose_name=b'Group')),
                ('member_groups', models.ManyToManyField(to='projectaccess.P4Group')),
                ('member_users', models.ManyToManyField(to='projectaccess.P4User')),
            ],
        ),
        migrations.AddField(
            model_name='metaproject',
            name='p4_group',
            field=models.OneToOneField(null=True, to='projectaccess.P4Group'),
        ),
    ]
