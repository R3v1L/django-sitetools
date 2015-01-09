#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Site tools validators module
===============================================

.. module:: sitetools.validators
    :platform: Django
    :synopsis: Site tools validators module
.. moduleauthor:: (C) 2015 Oliver Gutiérrez
"""

# Django imports
from django.utils.translation import ugettext
from django.template import Template, Context
from django.core.validators import ValidationError

def django_template_code_validator(value):
	"""
	Django template code validator
	"""
	try:
		Template(value).render(Context({}))
	except Exception,e:
		raise ValidationError(ugettext('Error trying to render template code: %s') % e)
