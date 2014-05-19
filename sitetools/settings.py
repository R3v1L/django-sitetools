# -*- coding: utf-8 -*-
"""
Django site tools application default settings
===============================================

.. module:: sitetools.settings
    :platform: Django
    :synopsis: Django site tools application default settings
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Specifies if the site is under maintenance
SITETOOLS_UNDER_MAINTENANCE = False

# Whitelist of URLs that will not check maintenance mode
SITETOOLS_MAINTENANCE_WHITELIST=()

# URLs allowed to use HTTPS
SITETOOLS_ALLOWED_SECURE_URLS=(r'^/.*$',)

# URLs forced to use HTTPS
SITETOOLS_FORCED_SECURE_URLS=()

# Case sensitive URLs
SITETOOLS_CASE_SENSITIVE_URLS=()

