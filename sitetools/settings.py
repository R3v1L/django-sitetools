# -*- coding: utf-8 -*-
"""
Django site tools application default settings
===============================================

.. module:: sitetools.settings
    :platform: Django
    :synopsis: Django site tools application default settings
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Static sendfile backend
STATIC_SENDFILE_BACKEND = 'mod_xsendfile'

# Site under maintenance
SITE_UNDER_MAINTENANCE = False

# URLs that will not check maintenance mode
MAINTENANCE_URL_WHITELIST = ()

# URLs allowed to use HTTPS
ALLOWED_SECURE_URLS = (r'^/.*$',)

# URLs forced to use HTTPS
FORCED_SECURE_URLS = ()

# Use secure URLs in debug mode
SECURE_URLS_DEBUG = False

# Case sensitive URLs
CASE_SENSITIVE_URLS = ()

# View for legal documents acceptance
LEGAL_DOCUMENT_ACCEPTANCE_VIEW = 'sitetools.views.legal_document_acceptance'

# View for legal documents
LEGAL_DOCUMENT_VIEW = 'sitetools.views.legal_document_view'

# Force legal documents acceptance by user
FORCE_LEGAL_ACCEPTANCE = True

# URLs that will not force legal documents acceptance (Admin site, logout, etc.)
FORCE_LEGAL_ACCEPTANCE_WHITELIST_URLS = ('/admin/','/accounts/logout/')

# Legal documents forced acceptance document
FORCED_LEGAL_DOCUMENT = None

# Legal documents forced acceptance document version
FORCED_LEGAL_DOCUMENT_VERSION = None

# Site log level for mailing administrators
SITE_LOG_MAIL_ADMINS_LEVEL = 0

SHOW_PREVIOUS_LEGAL_DOCUMENT_VERSIONS = False