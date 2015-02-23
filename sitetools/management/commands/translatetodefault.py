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

	option_list = BaseCommand.option_list + (
        make_option('--fullreplace',
            action='store_true',
            dest='fullreplace',
            default=False,
            help=_('Replace existing translations too')
        ),
        make_option('--savemo',
            action='store_true',
            dest='savemo',
            default=False,
            help=_('Replace existing translations too')
        ),
    )

	def handle(self, *args, **options):
		"""
		Command handling
		"""
		if not args:
			raise CommandError(_('You must specify at least one language to process'))
		for lang in args:
			filename='locale/%s/LC_MESSAGES/django.po' % lang
			try:	
				po = polib.pofile(filename)
				for entry in po:
					if options['fullreplace'] or not entry.msgstr:
						entry.msgstr=entry.msgid
				po.save()
				if options['savemo']:
					po.save_as_mofile('locale/%s/LC_MESSAGES/django.mo' % lang)
			except Exception, e:
				self.stdout.write(_('ERROR: Can not open %(filename)s: %(error)s\n') % (filename,e))
				# raise CommandError(_('Unexpected error raising anunciosx.com advertisements: %s') % e)
