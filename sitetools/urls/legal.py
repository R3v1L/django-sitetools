# -*- coding: utf-8 -*-
"""
Legal documents application URLs module
===============================================

.. module:: sitetools.urls.legal
    :platform: Django
    :synopsis: Sitetools legal URLs module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    # Legal document acceptance pages
    url(r'^accept/(?P<docid>\w+)/(?P<version>\w+)/$',
        settings.LEGAL_DOCUMENT_ACCEPTANCE_VIEW,
        name='legal_document_acceptance_version'),
    url(r'^accept/(?P<docid>\w+)/$',
        settings.LEGAL_DOCUMENT_ACCEPTANCE_VIEW,
        name='legal_document_acceptance_latest'),
    url(r'^accept/$',
        settings.LEGAL_DOCUMENT_ACCEPTANCE_VIEW,
        name='legal_document_acceptance_default'),

    # Legal document view
    url(r'^(?P<docid>\w+)/(?P<version>\w+)/$', 
        settings.LEGAL_DOCUMENT_VIEW,
       name='legal_document_version'),
    url(r'^(?P<docid>\w+)/$',
        settings.LEGAL_DOCUMENT_VIEW,
       name='legal_document_latest'),
    url(r'^$',
        settings.LEGAL_DOCUMENT_VIEW,
        name='legal_document_default'),
]
