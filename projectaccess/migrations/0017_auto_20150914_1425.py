# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0016_auto_20150910_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ldapuser',
            name='cn',
        ),
        migrations.RemoveField(
            model_name='ldapuser',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='ldapuser',
            name='uid',
        ),
        migrations.AddField(
            model_name='ldapuser',
            name='pa_user',
            field=models.OneToOneField(null=True, to='projectaccess.PAUser'),
        ),
        migrations.AddField(
            model_name='pauser',
            name='p4_user_name',
            field=models.CharField(default='', max_length=1024, verbose_name=b'P4UserName'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ldapuser',
            name='dn',
            field=models.CharField(max_length=1024, verbose_name=b'dn'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
