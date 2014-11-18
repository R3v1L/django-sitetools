# -*- coding: utf-8 -*-
"""
Remote content getter template tag
===============================================

.. module:: sitetools.templatetags.sitetools.tags.remote_content
    :platform: Django
    :synopsis: Remote content getter template tag
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Python imports
import urllib, warnings

# Try to import cssselect module
try:
    from pyquery import PyQuery
except ImportError:
    warnings.warn('PyQuery module not available. Selectors will be ignored in remote_content template tag',ImportWarning)
    PyQuery=None

# Django imports
from django import template
from django.conf import settings

class RemoteContentNode(template.Node):
    """
    Template node for remote_content tag
    """
    def __init__(self, url, selector=None):
        """
        Template node initialization
        """
        self.selector=None
        if selector is not None:
            self.selector=template.Variable(selector)
        self.url = template.Variable(url)

    def render(self, context):
        """
        Template node rendering method
        """
        try:
            url=self.url.resolve(context)
            resp=urllib.urlopen(url).read()
            if self.selector is not None:
                if PyQuery is not None:
                    pq=PyQuery(resp)
                    resp=pq(self.selector).html()
                else:
                    warnings.warn('PyQuery module not available. Selector has been ignored in remote_content template tag',RuntimeWarning)
            return resp 
        except Exception,e:
            if settings.DEBUG_TEMPLATE:
                return unicode(e)

def remote_content_tag(parser, token):
    """
    Tag compilation function
    """
    # Manage parameters
    parms=token.split_contents()
    l=len(parms)
    if l == 2:
        tagname, url = parms
        selector = None
    elif l == 3:
        tagname, url, selector = parms
    else:
        tagname=token.contents.split()[0]
        raise template.TemplateSyntaxError, "%r tag parameters error. Syntax: %r url [css_selector]" % (tagname,tagname)
    # Return template node
    return RemoteContentNode(url,selector)

