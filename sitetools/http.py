# -*- coding: utf-8 -*-
"""

===============================================

.. module:: sitetools.http
    :platform: Unix, Windows
    :synopsis: 
    :deprecated:
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import json

# Django imports
from django.http import HttpResponse

class HttpResponseServiceUnavailable(HttpResponse):
    """
    ** Subclass for HttpResponse with 503 status code**

    """
    status_code = 503

class JSONResponse(HttpResponse):
    """
    **JSON response class**
    
    *Django HttpResponse with support for JSON response*
    """
    def __init__(self,data,*args,**kwargs):
        """
        Class initialization method

        :param data: Data to be serialized to JSON and added to response
        :type data: List or dictionary
        """
        content=json.dumps(data)
        kwargs.setdefault('content_type','text/plain')
        # Call parent initialization
        super(JSONResponse,self).__init__(content,*args,**kwargs)