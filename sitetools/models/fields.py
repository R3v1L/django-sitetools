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

# Application imports
from sitetools import enums
from sitetools.forms.fields import LocationFormField

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
        try:
            return json.loads(value)
        except:
            # Encode current value as JSON and return it
            return json.dumps([value])

class LocationField(JSONField):
    """
    Location field class
    """
    description = _('JSON encoded latitude and longitude')
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        return super(LocationField,self).formfield(form_class=LocationFormField,**kwargs)

    def contribute_to_class(self, cls, name):
        """
        Contribute to class adding get_FIELD_display method to the model containing this field
        """
        def get_location_display(modelobj,lang=None):
            """
            Function to show location coordinates
            """
            data=getattr(modelobj,name)
            if data:
                return '(%s,%s)' % (data['lat'],data['lon'])
            return None
        
        # TODO: Set verbose name for field in short description for display method
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #getattr(cls, 'get_%s_display' % name).short_description=getattr(cls,name).short_description

        # Set attribute
        setattr(cls, 'get_%s_display' % name, get_location_display)
        
        # Call original method
        super(LocationField,self).contribute_to_class(cls, name)