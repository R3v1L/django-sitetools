# -*- coding: utf-8 -*-
"""

===============================================

.. module:: sitetools.template.response
    :platform: Unix, Windows
    :synopsis: 
    :deprecated:
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.utils import six
from django.utils._os import safe_join
from django.template.response import TemplateResponse
from django.conf import settings

# Application imports
from sitetools.utils import get_site_from_request

class SiteTemplateResponse(TemplateResponse):
    """
    Template response that uses a site specific template if available
    """
    def resolve_template(self, template):
        """
        Accepts a template object, path-to-template or list of paths.
        It adds automatically the site specific part of the template path
        if template is a string or a list of templates 
        """
        # Get current site from request
        try:
            site=self._request.site
        except:
            site=get_site_from_request(self._request)
        prefix=safe_join(settings.SITE_TEMPLATE_PREFIX,site.domain)
        if isinstance(template, six.string_types):
            # Convert single template in a list of templates with the site one
            template=[safe_join(prefix,template), template]
        elif isinstance(template, (list, tuple)):
            templatelist=[]
            # Add the site specific template before every template listed
            for t in template:
                templatelist.append(safe_join(prefix,t))
                templatelist.append(t)
            template=templatelist
        # Call parent method
        return super(SiteTemplateResponse,self).resolve_template(template)