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

from sitetools import views

urlpatterns = [
    # Legal document acceptance pages
    url(r'^accept/(?P<docid>\w+)/(?P<version>\w+)/$',
        views.legal_document_acceptance,
        name='legal_document_acceptance_version'),
    url(r'^accept/(?P<docid>\w+)/$',
        views.legal_document_acceptance,
        name='legal_document_acceptance_latest'),
    url(r'^accept/$',
        views.legal_document_acceptance,
        name='legal_document_acceptance'),

    # Legal document view
    url(r'^(?P<docid>\w+)/(?P<version>\w+)/$', 
        views.legal_document_view,
       name='legal_document_version'),
    url(r'^(?P<docid>\w+)/$',
        views.legal_document_view,
       name='legal_document_latest'),
    url(r'^$',
        views.legal_document_view,
        name='legal_document'),
]
