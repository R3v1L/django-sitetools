# -*- coding: utf-8 -*-
"""

===============================================

.. module:: evodjango.i18n.forms.fields
    :platform: Django
    :synopsis: 
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# EVODjango imports
from sitetools.i18n.forms.widgets import *

class I18NField(forms.MultiValueField):
    """
    Internationalized character field
    """
    base_field=forms.CharField
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        require_all_fields=kwargs.pop('require_all_fields',False)
        if require_all_fields:
            incompletemsg=_('Please, fill all translations')
        else:
            incompletemsg=_('Please, fill at least main language field (%s)' % dict(settings.LANGUAGES)[settings.LANGUAGE_CODE])
        error_messages = {
            'incomplete': incompletemsg,
        }
        fields=[]
        max_length=kwargs.pop('max_length',None)
        for lang,langname in settings.LANGUAGES:
            field_args={
                'required': require_all_fields or settings.LANGUAGE_CODE==lang,
                'max_length': max_length,
            }
            field=self.base_field(**field_args)
            fields.append(field)
        
        kwargs['widget']=I18NWidget(kwargs['widget'] for lang in settings.LANGUAGES)
        super(I18NField, self).__init__(error_messages=error_messages, fields=fields, require_all_fields=require_all_fields, *args, **kwargs)

    def compress(self,data_list):
        """
        Data compression method
        """
        data={}
        for lang,value in zip([code for code,langname in settings.LANGUAGES],data_list):
            data[lang]=value
        return data
