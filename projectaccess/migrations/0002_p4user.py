# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='P4User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=1024, verbose_name=b'User')),
                ('email', models.CharField(max_length=1024, verbose_name=b'E-Mail')),
                ('full_name', models.CharField(max_length=1024, verbose_name=b'Full Name')),
            ],
        ),
    ]
