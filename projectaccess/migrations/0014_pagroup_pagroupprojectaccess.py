# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0013_auto_20150907_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name=b'Name')),
                ('members', models.ManyToManyField(to='projectaccess.PAUser')),
            ],
        ),
        migrations.CreateModel(
            name='PAGroupProjectAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='projectaccess.PAGroup')),
                ('project', models.ForeignKey(to='projectaccess.PAProject')),
            ],
        ),
    ]
