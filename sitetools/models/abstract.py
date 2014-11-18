#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sitetools abstract models module
===============================================

.. module:: sitetools.models.abstract
    :platform: Django
    :synopsis: Sitetools abstract models module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

# Generic model base class
class GenericModel(models.Model):
    """
    Generic relation model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True
    
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),
        help_text=_('Associated object identifier'))
    content_object = GenericForeignKey('content_type', 'object_id')

class GenericNullModel(models.Model):
    """
    Generic relation model
    """
    class Meta:
        """
        Metadata for this model
        """
        abstract=True
    
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),blank=True,null=True,
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),blank=True,null=True,
        help_text=_('Associated object identifier'))
    content_object = GenericForeignKey('content_type', 'object_id')