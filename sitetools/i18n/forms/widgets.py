# -*- coding: utf-8 -*-
"""

===============================================

.. module:: evodjango.i18n.forms.widgets
    :platform: Django
    :synopsis: 
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django import forms
from django.conf import settings

class I18NWidget(forms.MultiWidget):
    """
    Internationalized input widget
    """
    def __init__(self,widgets,attrs=None):
        """
        Initialization method
        """
        super(I18NWidget,self).__init__(widgets=widgets,attrs=attrs)

    def decompress(self,value):
        """
        Decompress value
        """
        data_list=[]
        if value:
            for lang,langname in settings.LANGUAGES:
                if lang in value:
                    data_list.append(value[lang])
                else:
                    data_list.append(None)
        return data_list

    def format_output(self,rendered_widgets):
        """
        Return formatted output            
        """
        return '<table>' + ' '.join(['<tr><td>%s</td><td>%s</td></tr>' % data for data in zip([langname for lang,langname in settings.LANGUAGES],rendered_widgets)]) + '</table>'
