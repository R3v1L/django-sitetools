# -*- coding: utf-8 -*-
"""
Site tools template filters
===============================================

.. module:: sitetools.templatetags.filters
    :platform: Django
    :synopsis: Site tools template filters
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""
# Python imports
import random
import base64
import datetime

# Django imports
from django.conf import settings
from django import template
from django.utils.translation import ugettext

def dict_lookup(d, key):
    """
    Return dictionary value for given key
    """
    return d[key]

def shuffle_list(arg):
    """
    Return a shuffled copy of a list
    """
    tmp = arg[:]
    random.shuffle(tmp)
    return tmp

def call_method(obj, methodName):
    """
    Execute a method of an object using previously passed arguments with setarg filter
    """
    method = getattr(obj, methodName)
    if hasattr(obj, '__call_arguments'):
        ret = method(*obj.__call_arguments)
        del obj.__call_arguments
        return ret
    return method()
     
def set_arg(obj, arg):
    """
    Pass an argument 
    """
    if not hasattr(obj, '__call_arguments'):
        obj.__call_arguments = []
    obj.__call_arguments += [arg]
    return obj

def get_range(value):
    """
    Return a range of numbers for given value as python range does
    """
    return range(value)

def without_lang(value):
    """
    Removes language part from given
    """
    for lang,langname in settings.LANGUAGES:
        if value.startswith('/' + lang + '/'):
            value=value[len(lang)+1:]
            break
    return value

def b64encode(value):
    """
    Encode a value in base64
    """
    return base64.b64encode(value)

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string
    """
    htmlcodes=(
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in htmlcodes:
        s = s.replace(code[1], code[0])
    return s

def month_name(number):
    """
    Return month name from a number between 1-12
    """
    return ugettext(datetime.datetime.strptime(str(number), "%m").strftime('%B'))
    