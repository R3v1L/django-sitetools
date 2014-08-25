# -*- coding: utf-8 -*-
"""

===============================================

.. module:: evodjango.i18n.models
    :platform: Django
    :synopsis: 
.. moduleauthor:: (C) 2014 Oliver Gutiérrez

# TODO: Automatic translation support using Google Translate
"""

# Django imports
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _
from django.utils.functional import curry
from django.conf import settings
from django import forms

# EVODjango imports
from sitetools.models import JSONField
from sitetools.forms.widgets import TinyMCEWidget
from sitetools.i18n.forms import I18NField

class I18NTextField(JSONField):
    """
    Internationalization TextField
    """
    description = _('Internationalization TextField')
    __metaclass__ = models.SubfieldBase
    
    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        kwargs.setdefault('required',not self.blank)
        kwargs.setdefault('label',self.verbose_name)
        return I18NField(**kwargs)

    def contribute_to_class(self, cls, name):
        """
        Contribute to class adding localized_FIELD methods to the model containing this field
        """
        def get_localized_version(modelobj,lang=None):
            """
            Function to show localized version of a field
            """
            data=getattr(modelobj,name)
            if lang is None:
                lang=get_language()
            if lang in data:
                return data[lang]
            return ''
        
        setattr(cls, 'localized_%s' % name, get_localized_version)
        for lang,langname in settings.LANGUAGES:
            setattr(cls, 'localized_%s_%s' % (name,lang), curry(get_localized_version,lang=lang))

        # Call original method
        super(I18NTextField,self).contribute_to_class(cls, name)

class I18NCharField(I18NTextField):
    """
    Internationalization CharField
    """
    description = _('Internationalization CharField')
    __metaclass__ = models.SubfieldBase
    
    def formfield(self,**kwargs):
        """
        Form field method overload
        """
        kwargs.setdefault('max_length',self.max_length)
        kwargs['widget']=forms.TextInput
        return super(I18NCharField,self).formfield(**kwargs)

class I18NHTMLField(I18NTextField):
    """
    Internationalization HTMLField
    """
    description = _('Internationalization HTMLField')
    __metaclass__ = models.SubfieldBase
    
    def formfield(self,**kwargs):
        """
        Form field method overload
        """
        kwargs['widget']=TinyMCEWidget
        return super(I18NHTMLField,self).formfield(**kwargs)
