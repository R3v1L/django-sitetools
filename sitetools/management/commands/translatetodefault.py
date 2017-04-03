#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Site tools command for translating po files to default values
===============================================

.. module:: sitetools.management.commands.translatetodefault
    :platform: Django
    :synopsis: Site tools command for translating po files to default values
.. moduleauthor:: (C) 2015 Oliver Gutiérrez
"""

# Python imports
from optparse import make_option
import polib

# Django imports
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings


class Command(BaseCommand):
    args = '<lang lang ...>'
    help = _('Set translations to default translation string')

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('lang', nargs='+', type=str)

        # Named (optional) arguments
        parser.add_argument(
            '--fullreplace',
            action='store_true',
            dest='fullreplace',
            default=False,
            help=_('Replace existing translations too')
        )
        parser.add_argument(
            '--savemo',
            action='store_true',
            dest='savemo',
            default=False,
            help=_('Save .mo file')
        )

    def handle(self, *args, **options):
        """
        Command handling
        """
        for lang in options['lang']:
            filename = 'locale/%s/LC_MESSAGES/django.po' % lang
            try:
                po = polib.pofile(filename)
                for entry in po:
                    if options['fullreplace'] or not entry.msgstr:
                        entry.msgstr = entry.msgid
                po.save()
                if options['savemo']:
                    po.save_as_mofile('locale/%s/LC_MESSAGES/django.mo' % lang)
            except Exception, e:
                self.stdout.write(
                    _('ERROR: Can not open %s: %s\n') % (filename, e))
