# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sitetools.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitetools', '0003_auto_20150130_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitelog',
            name='data',
            field=sitetools.models.fields.JSONField(default=b'"\\"null\\""', help_text='Extra data for log message', null=True, verbose_name='Data', blank=True),
        ),
        migrations.AlterField(
            model_name='sitevar',
            name='type',
            field=models.CharField(default=b'unicode', help_text='Variable type', max_length=15, verbose_name='Type', choices=[(b'unicode', 'Unicode string'), (b'int', 'Integer'), (b'float', 'Floating point number'), (b'bool', 'Boolean'), (b'list', 'List'), (b'json', 'JSON data')]),
        ),
    ]
