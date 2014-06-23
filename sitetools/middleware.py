# -*- coding: utf-8 -*-
"""

===============================================

.. module:: sitetools.middleware
    :platform: Django
    :synopsis: 
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import re

# Django imports
from django.conf import settings, urls
from django.core import urlresolvers
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
from django.middleware.locale import LocaleMiddleware

# Application imports
from sitetools.models import LegalDocument
from sitetools.utils import match_any, get_site_from_request, get_client_ip, build_site_url

# Add 503 handler to django urls module
urls.handler503 = 'sitetools.views.service_unavailable'
urls.__all__.append('handler503')

class CurrentSiteMiddleware(object):
    """
    Enhanced Middleware that sets `site` attribute to request object by checking host against the Site model domains
    """
    def process_request(self, request):
        """
        Request processing method
        """
        site = get_site_from_request(request)
        request.site = site

class MaintenanceMiddleware(object):
    """
    Middleware that checks for maintenance on current site and returns Service Unavailable response
    """
    
    # Compile maintenance whitelist URLs
    _MAINTENANCE_WHITELIST = tuple([re.compile(u) for u in settings.MAINTENANCE_URL_WHITELIST]) 
    
    def process_request(self, request):
        """
        Request processing method
        """
        try:
            site=request.site
        except:
            # Get current site
            site = get_site_from_request(request)
        try:
            sitemaintenance=site.siteinfo.maintenance
        except:
            sitemaintenance=False
            
        # Check if site is not marked as under maintenance or forced maintenance is specified
        if settings.SITE_UNDER_MAINTENANCE or sitemaintenance:
            # Allow access if client IP is in INTERNAL_IPS or logged in user is staff member
            if get_client_ip(request) not in settings.INTERNAL_IPS and not request.user.is_staff:
                # Check if current view is whitelisted
                if not match_any(request.path_info, self._MAINTENANCE_WHITELIST):
                    # Return 503 handler response
                    resolver = urlresolvers.get_resolver(None)
                    callback, param_dict = resolver._resolve_special('503')
                    return callback(request, **param_dict)

class SecureURLMiddleware(object):
    """
    Middleware that checks security for current request path and redirects if needed
    """

    # Compile forced secure URLs list
    _forced_secure_urls = tuple([re.compile(u) for u in settings.FORCED_SECURE_URLS])
    
    # Compile secure URLs list
    _allowed_secure_urls = _forced_secure_urls + tuple([re.compile(u) for u in settings.ALLOWED_SECURE_URLS])
    
    def process_request(self, request):
        """
        Request processing method
        """
        if hasattr(request, 'site'):
            site=request.site
        else:
            # Get current site
            site = get_site_from_request(request)
            
        # Only check security if debug is disabled
        if not request.is_secure():
            # Force HTTPS for forced secure paths
            if match_any(request.path_info, self._forced_secure_urls):
                return redirect(build_site_url(site,request.get_full_path(),secure=True))
        else:
            # Allow secure paths only for allowed ones
            if not match_any(request.path_info, self._allowed_secure_urls):
                return redirect(build_site_url(site,request.get_full_path(),secure=False))

class CaseInsensitiveURLMiddleware(object):
    """
    Middleware for having case insensitive URLs 
    """
    
    # Compile case sensitive paths
    _case_sensitive_paths = tuple([re.compile(u) for u in settings.CASE_SENSITIVE_URLS])
    
    def process_request(self, request):
        """
        Request processing method
        """
        lpath=request.path_info.lower()
        if request.path_info != lpath and not match_any(request.path_info, self._case_sensitive_paths):
            return redirect(lpath,permanent=False)
        return None

class LegalMiddleware(object):
    """
    Legal documents middleware class
    """
    def process_request(self, request):
        """
        Request processing
        """
        if settings.FORCE_LEGAL_ACCEPTANCE:
            # Check media and static URLs
            if request.path.startswith(settings.MEDIA_URL) or request.path.startswith(settings.STATIC_URL):
                return None
            # Check URL whitelist
            for path in settings.FORCE_LEGAL_ACCEPTANCE_WHITELIST_URLS:
                    if request.path.startswith(path):
                        return None
            # Check if user is logged in and accessing other URL different to legal acceptance 
            if request.user.is_authenticated() and not request.path.startswith(urlresolvers.reverse('legal_document_acceptance')):
                document=LegalDocument.get_document_version(settings.FORCED_LEGAL_DOCUMENT, settings.FORCED_LEGAL_DOCUMENT_VERSION)
                if document is not None:
                    # Check if current user accepted the document
                    if document.accepted_by_user(request.user) is None:
                        # Redirect to acceptance page
                        if settings.FORCED_LEGAL_DOCUMENT is not None:
                            if settings.FORCED_LEGAL_DOCUMENT_VERSION is not None:
                                return redirect(urlresolvers.reverse('legal_document_acceptance_version',args=[settings.FORCED_LEGAL_DOCUMENT, settings.FORCED_LEGAL_DOCUMENT_VERSION]))
                            else:
                                return redirect(urlresolvers.reverse('legal_document_acceptance_latest',args=[settings.FORCED_LEGAL_DOCUMENT]))
                        return redirect(urlresolvers.reverse('legal_document_acceptance') + '?next=' + request.path)

class SEOFriendlyLocaleMiddleware(LocaleMiddleware):
    """
    SEO Friendly locale middleware
    """
    response_redirect_class = HttpResponsePermanentRedirect