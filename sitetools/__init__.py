# -*- coding: utf-8 -*-
"""
Django site tools application
===============================================

.. module:: sitetools
    :platform: Django
    :synopsis: Django site tools application
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Application imports
from sitetools.utils import inject_app_defaults

# Default application settings injection
inject_app_defaults(__name__)