# -*- coding: utf-8 -*-
"""
Sitetools utility functions module
===============================================

.. module:: sitetools.utils
    :platform: Django
    :synopsis: Sitetools utility functions module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import sys

# Django imports
from django.contrib.sites.models import Site
from django.utils import six

def inject_app_defaults(appname):
    """
    Inject an application's default settings
    """
    try:
        # Import application settings module
        __import__('%s.settings' % appname)
        # Import our defaults, project defaults, and project settings
        _app_settings = sys.modules['%s.settings' % appname]
        _def_settings = sys.modules['django.conf.global_settings']
        _settings = sys.modules['django.conf'].settings
        # Add the values from the application settings module
        for _k in dir(_app_settings):
            if _k.isupper():
                # Add the value to the default settings module
                setattr(_def_settings, _k, getattr(_app_settings, _k))
                
                # Add the value to the settings, if not already present
                if not hasattr(_settings, _k):
                    setattr(_settings, _k, getattr(_app_settings, _k))
    except ImportError:
        # Silently skip failing settings modules
        pass

def get_client_ip(req):
    """
    Get client IP address from a request
    """
    # Public IP discovering
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        ip=req.META['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
    else:
        ip=req.META['REMOTE_ADDR']
    return ip

def get_site_from_request(request):
        # By default, our site will be the one we defined in settings
        site=Site.objects.get_current()
        # Get request host
        hostname=request.get_host()
        sites=Site.objects.filter(domain=hostname)
        if sites.count() > 0:
            site=sites[0]
        return site

def build_site_url(site,url,secure=False):
    """
    Build an absolute URL for a given site
    """
    protocol='http'
    if secure:
        protocol='https'
    print u'%s://%s%s' % (protocol,site.domain,url)
    return u'%s://%s%s' % (protocol,site.domain,url)

def match_any(text,patternlist):
    """
    Checks if text matches any of given strings or regexp list
    """
    for pattern in patternlist:
        if (isinstance(pattern,six.string_types) and text == pattern) or pattern.match(text):
            return True 
    return False

