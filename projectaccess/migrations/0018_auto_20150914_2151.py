# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectaccess', '0017_auto_20150914_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pa_user', models.OneToOneField(null=True, to='projectaccess.PAUser')),
            ],
        ),
        migrations.AddField(
            model_name='paproject',
            name='p4_template_workspace',
            field=models.CharField(default='', max_length=1024, verbose_name=b'P4TemplateWorkspace'),
            preserve_default=False,
        ),
    ]
