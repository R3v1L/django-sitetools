# -*- coding: utf-8 -*-
"""
Site tools form fields module
===============================================

.. module:: sitetools.forms.fields
    :platform: Django
    :synopsis: Site tools form fields module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""
# Django imports
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class EULAField(forms.Field):
    """
    EULA agreement form field class
    """
    def __init__(self,eula_url=None,*args,**kwargs):
        """
        Class initialization
        """
        if not 'label' in kwargs:
            if eula_url:
                label=kwargs.get('label',_('I accept the <a href="%s" target="_blank">terms and conditions</a>') % eula_url)
            else:
                label=kwargs.get('label',_('I accept the terms and conditions') % eula_url)
        kwargs['label']=mark_safe(label)
        kwargs.setdefault('widget',forms.CheckboxInput())
        super(EULAField,self).__init__(*args,**kwargs)

    def clean(self,value):
        """
        Check if user has accepted the EULA
        """
        if not value:
            raise forms.ValidationError(_('You have to accept the terms and conditions to continue'))

