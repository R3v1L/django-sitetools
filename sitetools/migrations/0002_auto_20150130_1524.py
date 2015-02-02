# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sitetools.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitetools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitelog',
            name='data',
            field=sitetools.models.fields.JSONField(default=b'"\\"null\\""', help_text='Extra data for log message', null=True, verbose_name='Data', blank=True),
        ),
    ]
