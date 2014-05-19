# -*- coding: utf-8 -*-
"""
 models module
===============================================

.. module:: sitetools.models
    :platform: Django
    :synopsis: models module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports

# Django imports
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

# Applications imports

class SiteInfo(models.Model):
    """
    Site information model
    """
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Site information')
        verbose_name_plural=_('Site information')
    
    site=models.OneToOneField(Site,verbose_name=_('Site'),
        help_text=_('Site this information is bound to'))
    maintenance=models.BooleanField(_('Maintenance'),default=False,
        help_text=_('Specify if this site is currently under maintenance'))
    active=models.BooleanField(_('Active'),default=False,
        help_text=_('Specifies if this site is currently active'))
    
