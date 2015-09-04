# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0010_metaproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name=b'Name')),
                ('p4_path', models.CharField(max_length=1024, verbose_name=b'P4Path')),
            ],
        ),
        migrations.CreateModel(
            name='PAUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name=b'Name')),
            ],
        ),
        migrations.CreateModel(
            name='PAUserProjectAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='projectaccess.PAUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='metaproject',
            name='members',
        ),
        migrations.RemoveField(
            model_name='metaproject',
            name='p4_group',
        ),
        migrations.RemoveField(
            model_name='metauser',
            name='ldap_user',
        ),
        migrations.RemoveField(
            model_name='metauser',
            name='p4_user',
        ),
        migrations.RemoveField(
            model_name='p4group',
            name='member_subgroups',
        ),
        migrations.RemoveField(
            model_name='p4group',
            name='member_users',
        ),
        migrations.DeleteModel(
            name='MetaProject',
        ),
        migrations.DeleteModel(
            name='MetaUser',
        ),
        migrations.DeleteModel(
            name='P4Group',
        ),
        migrations.DeleteModel(
            name='P4User',
        ),
        migrations.AddField(
            model_name='paproject',
            name='users_with_access',
            field=models.ManyToManyField(to='projectaccess.PAUserProjectAccess'),
        ),
    ]
