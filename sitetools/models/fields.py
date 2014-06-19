# -*- coding: utf-8 -*-
"""
Site tools model fields
===============================================

.. module:: sitetools.models.fields
    :platform: Django
    :synopsis: Site tools model fields module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""
# Python imports
import json

# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# EVODjango imports
from sitetools import enums

class CountryField(models.CharField):
    """
    Country selection field
    """
    description = _('Country selection field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', enums.COUNTRIES)
        super(CountryField, self).__init__(*args, **kwargs)

class LanguageField(models.CharField):
    """
    Language selection field
    """
    description = _('Language selection field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', settings.LANGUAGES)
        super(LanguageField, self).__init__(*args, **kwargs)

class EncodedField(models.TextField):
    """
    Encoded data field
    """
    description = _('Encoded data field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self,*args, **kwargs):
        """
        Initialization method
        """
        self.encodecb=kwargs.pop('encoder',None)
        if self.encodecb is None:
            raise ValueError(_('No encoder callback defined'))
        self.decodecb=kwargs.pop('decoder',None)
        if self.decodecb is None:
            raise ValueError(_('No decoder callback defined'))
        super(EncodedField,self).__init__(*args, **kwargs)
    
    def dummy_encode_decode(self,value):
        """
        Dummy enconde/decode method for raising not implemented error
        """

    def to_python(self,value):
        """
        Python object casting method
        """
        return self.decodecb(value)

    def get_prep_value(self,value):
        """
        DB object casting method
        """
        return self.encodecb(value)

class JSONField(EncodedField):
    """
    JSON data field
    """
    description = _('JSON encoded data field')
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        kwargs.setdefault('default', [])
        super(JSONField,self).__init__(encoder=json.dumps,decoder=self.decode_json, *args, **kwargs)
    
    def decode_json(self,value):
        """
        Python object casting method
        """
        if not value:
            return []
        elif isinstance(value, (list,dict)):
            return value
        return json.loads(value)
