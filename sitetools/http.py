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
import os, json, mimetypes

# Django imports
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings

class HttpResponseServiceUnavailable(HttpResponse):
    """
    **Subclass for HttpResponse with 503 status code**
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

class StaticSendFileResponse(HttpResponse):
    """
    **Static serve response class**
    
    *Django HttpResponse for serving static content through xsendfile or xaccel*
    
    If the user is in debug mode then 
    """
    def __init__(self,filepath,backend=settings.STATIC_SENDFILE_BACKEND,download_as=None,force_backend=False,extra_headers={},*args,**kwargs):
        """
        Class initialization method

        :param filepath: File path you want to serve
        :type filepath: String
        :param backend: Backend you want to use for serving file contents
        :type backend: String
        :param download_as: Filename that will be used for download
        :type download_as: String
        :param force_backend: Force using backend on debug mode instead using django
        :raises: ValueError if an invalid backend is specified
        
        .. note:: Valid options for backend parameter are:
        
            * **mod_xsendfile**: Use Apache mod_xsendfile for serving the static file.
            * **nginx_xaccel**: Use nginx X-Accel-Redirect for serving the static file. You can pass extra parameters using extra_headers. Some useful parms are X-Accel-Limit-Rate, X-Accel-Buffering or X-Accel-Charset
        """
        # Guess file mimetype
        content_type=mimetypes.guess_type(filepath)[0]
        kwargs.setdefault('content_type',content_type)
 
        if settings.DEBUG and not force_backend:
            # Serve file directly
            wrapper = FileWrapper(file(filepath))
            super(StaticSendFileResponse,self).__init__(wrapper,*args,**kwargs)
            self['Content-Length'] = os.path.getsize(filepath)
        else:
            # Serve file using HTTP server
            super(StaticSendFileResponse,self).__init__(*args,**kwargs)       
            if backend=='mod_xsendfile':
                self['X-Sendfile'] = filepath
            elif backend=='nginx_xaccel':
                self['X-Accel-Redirect'] = filepath
            else:
                raise Exception('Invalid static serving backend "%s"' % backend)
        # Setup download headers
        if download_as:
            self['Content-Disposition'] = 'attachment; filename=%s' % download_as
        # Setup custom headers
        for k,v in extra_headers.items():
            self[k] = v