# -*- coding: utf-8 -*-
"""
Site tools template tags module
===============================================

.. module:: sitetools.templatetags.sitetools
    :platform: Django
    :synopsis: Site tools template tags module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django import template

# Application imports
from filters import shuffle_list,set_arg,call_method,get_range,without_lang,b64encode,html_decode,month_name,dict_lookup # currency_formatter,file_size_formatter
from tags.stringrender import stringrender_tag
from tags.remote_content import remote_content_tag
# Initialize template tag library
register = template.Library()

# Register filters
register.filter('range',get_range)
register.filter('lookup',dict_lookup)
register.filter('shuffle',shuffle_list)
#register.filter('currency',currency_formatter)
#register.filter('filesize',file_size_formatter)
register.filter('html_decode', html_decode)
register.filter('setarg', set_arg)
register.filter('callmethod', call_method)
register.filter('without_lang',without_lang)
register.filter('b64encode',b64encode)
register.filter('month_name',month_name)
# Register tags
register.tag('stringrender',stringrender_tag)
register.tag('remote_content',remote_content_tag)