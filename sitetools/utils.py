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
import sys, os, datetime

# Django imports
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext
from django.conf import settings

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
    return u'%s://%s%s' % (protocol,site.domain,url)

def match_any(text,patternlist):
    """
    Checks if text matches any of given strings or regexp list
    """
    for pattern in patternlist:
        if (isinstance(pattern,six.string_types) and text == pattern) or pattern.match(text):
            return True 
    return False


def send_mail_from_template(recipient_list,subject_template_name,email_template_name,
                            from_email=settings.DEFAULT_FROM_EMAIL,request=None,context={},
                            fail_silently=False,auth_user=None, auth_password=None, connection=None,html=False):
    """
    Send email rendering a template
    """
    if request:
        context.update(RequestContext(request))
    subject=render_to_string(subject_template_name, context)
    subject=''.join(subject.splitlines())
    message=render_to_string(email_template_name, context)
    send_mail(subject, message, from_email, recipient_list, fail_silently, auth_user, auth_password, connection)

def send_mail_to_admins(subject_template_name,email_template_name,request=None,context={},fail_silently=True):
    """
    Send email to administrators
    """
    if request:
        context.update(RequestContext(request))
    subject=render_to_string(subject_template_name, context)
    subject=''.join(subject.splitlines())
    message=render_to_string(email_template_name, context)
    mail_admins(subject, message, fail_silently=True)

def static_serve(filepath,download_as=None,*args,**kwargs):
    """
    Static serve tool function
    """
    if os.path.exists(filepath) and not os.path.isdir(filepath):
        from sitetools.http import StaticSendFileResponse
        return StaticSendFileResponse(filepath,download_as=download_as,*args,**kwargs)
    else:
        raise Http404(ugettext('Requested file "%s" does not exist') % filepath)

def generate_expiration_date(seconds=604800):
    """
    Generates an expiration date (default 7 days)
    """
    date = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    return date.strftime('%a, %d %b %Y %H:%M:%S GMT')

def last_file_modification_date(*args,**kwargs):
    try:
        mtime=os.path.getmtime(settings.STATIC_ROOT + kwargs['path'])
        return datetime.datetime.fromtimestamp(mtime)
    except:
        return datetime.datetime.now()