# -*- coding: utf-8 -*-
"""
Site tools widgets module
===============================================

.. module:: 
    :platform: Unix, Windows
    :synopsis: Site tools widgets module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django import forms
from django.utils.safestring import mark_safe

class RECAPTCHAWidget(forms.widgets.Input):
    """
    reCAPTCHA field widget
    """
    def __init__(self,api_server,pubkey,lang='en',theme='red',*args,**kwargs):
        """
        Initialization method
        """
        self.lang=lang
        self.theme=theme
        self.pubkey=pubkey
        self.api_server=api_server
        super(RECAPTCHAWidget,self).__init__(*args,**kwargs)
    
    def render(self, name, value, attrs={}):
        """
        Render method overload
        """
        return mark_safe(u"""
        <script type="text/javascript">var RecaptchaOptions = {theme : '%s',lang: '%s'};</script>
        <script type="text/javascript" src="%s/challenge?k=%s"></script>
        <noscript>
           <iframe src="%s/noscript?k=%s" width="500" height="300"></iframe>
           <br />
           <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
           <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
        </noscript>
        <input id="%s" type="text" name="recaptcha_django_field" value="" style="display: none;">
        """ % (self.theme,self.lang,self.api_server,self.pubkey,self.api_server,self.pubkey,attrs['id']))

    def value_from_datadict(self, data, files, name):
        """
        Obtaining data from form submission
        """
        return (data.get('recaptcha_challenge_field',None),data.get('recaptcha_response_field',None))

class TinyMCEWidget(forms.Textarea):
    """
    TinyMCE HTML editor widget
    """
    class Media:
        """
        Media class
        """
        extend = False
        js = ('//tinymce.cachefly.net/4.0/tinymce.min.js',)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'tinymce'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(TinyMCEWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        output=super(TinyMCEWidget, self).render(name, value, attrs)
        return mark_safe(output + "<script>tinymce.init({selector: '.tinymce', menubar:false, statusbar: false,});</script>")