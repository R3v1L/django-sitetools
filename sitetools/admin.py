# -*- coding: utf-8 -*-
"""
 Administration module
===============================================

.. module:: sitetools.admin
    :platform: Django
    :synopsis: administration module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.contrib import admin

# Application imports
from sitetools.models import SiteInfo

class SiteInfoAdmin(admin.ModelAdmin):
    """
    Administration class
    """
    # Admin parameters    
    list_display = ('site','active','maintenance')
    list_filter = ('active','maintenance')
    search_fields = ('site__domain','site__name')
    list_editable = ('active','maintenance')
    save_on_top = True
    list_per_page = 30

# Admin models registration
admin.site.register(SiteInfo, SiteInfoAdmin)
