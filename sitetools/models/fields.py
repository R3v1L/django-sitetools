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
import pytz

# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Application imports
from sitetools import enums
from sitetools import validators
from sitetools.forms import LocationFormField, TinyMCEField, VectorFormField

TIMEZONE_CHOICES = [(x, x) for x in pytz.all_timezones]


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


class TimezoneField(models.CharField):
    """
    Timezone selection field
    """
    description = _('Time zone selection field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Class initialization method
        """
        kwargs.setdefault('max_length', 35)
        kwargs.setdefault('choices', TIMEZONE_CHOICES)
        super(TimezoneField, self).__init__(*args, **kwargs)


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


class DjangoTemplateCodeCharField(models.CharField):
    """
    Django template code field class
    """
    description = _('Django template code character string field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        kwargs.setdefault('validators', [validators.django_template_code_validator])
        super(DjangoTemplateCodeCharField, self).__init__(*args, **kwargs)


class DjangoTemplateCodeTextField(models.TextField):
    """
    Django template code field class
    """
    description = _('Django template code text field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        kwargs.setdefault('validators', [validators.django_template_code_validator])
        super(DjangoTemplateCodeTextField, self).__init__(*args, **kwargs)


class HTMLField(models.TextField):
    """
    HTML field class
    """
    description = _('HTML field')
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        kwargs.setdefault('form_class', TinyMCEField)
        return super(HTMLField, self).formfield(**kwargs)


class CodeField(models.TextField):
    """
    Code field class
    """
    description = _('Code field')
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        #kwargs.setdefault('form_class', AceEditorField)
        return super(CodeField, self).formfield(**kwargs)


class EncodedField(models.TextField):
    """
    Encoded data field
    """
    description = _('Encoded data field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        self.encodecb = kwargs.pop('encoder', None)
        if self.encodecb is None:
            raise ValueError(_('No encoder callback defined'))
        self.decodecb = kwargs.pop('decoder', None)
        if self.decodecb is None:
            raise ValueError(_('No decoder callback defined'))
        kwargs['default'] = self.encodecb(kwargs['default'])
        super(EncodedField, self).__init__(*args, **kwargs)

    def dummy_encode_decode(self, value):
        """
        Dummy enconde/decode method for raising not implemented error
        """
        raise NotImplementedError()

    def to_python(self, value):
        """
        Python object casting method
        """
        return self.decodecb(value)

    def get_prep_value(self, value):
        """
        DB object casting method
        """
        return self.encodecb(value)


class JSONField(EncodedField):
    """
    JSON data field

    TODO: Add getattr overload to get fields inside JSON data
    """
    description = _('JSON encoded data field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        kwargs.setdefault('default', None)
        super(JSONField, self).__init__(encoder=json.dumps, decoder=self.decode_json, *args, **kwargs)

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        #kwargs.setdefault('form_class', AceEditorField)
        return super(JSONField, self).formfield(**kwargs)

    def decode_json(self, value):
        """
        Python object casting method
        """
        if value is None:
            return None
        if not value:
            return {}
        if isinstance(value, (list, dict)):
            return value
        try:
            return json.loads(value)
        except:
            # Encode current value as JSON and return it
            return json.dumps(value)


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
        kwargs.setdefault('form_class', LocationFormField)
        return super(LocationField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name):
        """
        Contribute to class adding get_FIELD_display method to the model containing this field
        """
        def get_location_display(modelobj):
            """
            Function to show location coordinates
            """
            data = getattr(modelobj, name)
            if data:
                return '(%s,%s)' % (data['lat'], data['lon'])
            return None

        # TODO: Set verbose name for field in short description for display method
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #get_location_display.short_description=getattr(cls,name).verbose_name
        #getattr(cls, 'get_%s_display' % name).short_description=getattr(cls,name).short_description

        # Set attribute
        setattr(cls, 'get_%s_display' % name, get_location_display)

        # Call original method
        super(LocationField, self).contribute_to_class(cls, name)


class VectorField(JSONField):
    """
    Bidimensional vector field class
    """
    description = _('JSON encoded bidimensional vector')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Initialization method
        """
        self.dimensions = kwargs.get('dimensions',2)
        if 'dimensions' in kwargs:
            del(kwargs['dimensions'])
        super(VectorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        Form field method overload
        """
        kwargs.setdefault('form_class', VectorFormField)
        kwargs.setdefault('dimensions', self.dimensions)
        return super(VectorField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name):
        """
        Contribute to class adding get_FIELD_display method to the model containing this field
        """
        def get_vector_display(modelobj):
            """
            Function to show location coordinates
            """
            data = getattr(modelobj, name)
            if data:
                return '(%s,%s)' % (data['x'], data['y'])
            return None

        # Set attribute
        setattr(cls, 'get_%s_display' % name, get_vector_display)
        # Call original method
        super(VectorField, self).contribute_to_class(cls, name)
