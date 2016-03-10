# -*- coding: utf-8 -*-
"""
Template string render tag module
===============================================

.. module:: sitetools.templatetags.sitetools.tags.stringrender
    :platform: Django
    :synopsis: Template string render tag module
.. moduleauthor:: (C) 2012 Oliver Gutiérrez
"""

# Django imports
from django import template
from django.conf import settings


class StringRenderNode(template.Node):

    """
    Template node for stringrender tag
    """

    def __init__(self, template_string):
        """
        Template node initialization
        """
        self.template_string = template.Variable(template_string)

    def render(self, context):
        """
        Template node rendering method
        """
        try:
            t = template.Template(self.template_string.resolve(context))
            return t.render(context)
        except Exception, e:
            if settings.DEBUG:
                print (e)
            return ''


def stringrender_tag(parser, token):
    """
    Tag compilation function
    """
    try:
        # Manage parameters
        tag_name, template_string = token.split_contents()
    except ValueError:
        # Raise template error if template get incorrect parameters
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    # Return template node
    return StringRenderNode(template_string)
