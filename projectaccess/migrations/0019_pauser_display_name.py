# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0018_auto_20150914_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='pauser',
            name='display_name',
            field=models.CharField(default='', max_length=1024, verbose_name=b'DisplayName'),
            preserve_default=False,
        ),
    ]
