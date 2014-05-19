# -*- coding: utf-8 -*-
"""
 views module
===============================================

.. module:: sitetools.views
    :platform: Django
    :synopsis: views module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.http import HttpResponse

# Application imports
from sitetools.utils import get_site_from_request

def service_unavailable(request,template_name='503.html'):
    """
    Default service unavailable view
    """
    return TemplateResponse(request,template_name,status=503)

def robots(request,options={}):
    """
    Robots view
    """
    # Global robots
    try:
        data=render_to_string('robots.txt',options)
    except IOError:
        data=''
    # Per site robots
    try:
        site=request.site
    except:
        # Get current site
        site = get_site_from_request(request)
    try:
        data+=site.siteinfo.robots
    except:
        pass
    # Return robots.txt
    return HttpResponse(data,mimetype='text/plain')