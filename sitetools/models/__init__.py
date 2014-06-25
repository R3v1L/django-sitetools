# -*- coding: utf-8 -*-
"""
 models module
===============================================

.. module:: sitetools.models
    :platform: Django
    :synopsis: models module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import sys
import traceback

# Django imports
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins as django_mail_admins
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Applications imports
from sitetools.utils import get_site_from_request
from sitetools.models.fields import CountryField, LanguageField, JSONField

class SiteInfo(models.Model):
    """
    Site information model
    """
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Site information')
        verbose_name_plural=_('Site information')
    
    site=models.OneToOneField(Site,verbose_name=_('Site'),
        help_text=_('Site this information is bound to'))
    maintenance=models.BooleanField(_('Maintenance'),default=False,
        help_text=_('Specify if this site is currently under maintenance'))
    active=models.BooleanField(_('Active'),default=False,
        help_text=_('Specifies if this site is currently active'))

class SiteLog(models.Model):
    """
    Web site log model
    """
    INFO=1
    WARNING=2
    ERROR=3
    CRITICAL=4
    DEBUG=5
        
    LOG_LEVELS=(
        (INFO,_('Info')),
        (WARNING,_('Warning')),
        (ERROR,_('Error')),
        (CRITICAL,_('Critical')),
        (DEBUG,_('Debug')),
    )
    
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Site log')
        verbose_name_plural=_('Site logs')
    
    timestamp=models.DateTimeField(_('Created'),auto_now_add=True,
        help_text=_('Creation date'))
    site=models.ForeignKey(Site,verbose_name=_('Site'),blank=True, null=True,
        help_text=_('Associated website'))
    level=models.PositiveIntegerField(_('Level'),default=1,choices=LOG_LEVELS,
        help_text=_('Log level'))
    tag=models.CharField(_('Tag'),max_length=20,default='django',
        help_text=_('Tag for identifying this log message sender'))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('User'),blank=True,null=True,
        help_text=_('Associated user'))
    ip=models.GenericIPAddressField(_('IP address'),default='0.0.0.0',
        help_text=_('Associated IP address'))
    message=models.CharField(_('Message'),max_length=200,
        help_text=_('Log message'))
    data=JSONField(_('Data'),blank=True,null=True,
        help_text=_('Extra data for log message'))
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),blank=True,null=True,
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),blank=True,null=True,
        help_text=_('Associated object identifier'))
    content_object = GenericForeignKey('content_type', 'object_id')

    @staticmethod
    def log(tag,message,data=None,level=INFO,content_object=None,request=None,ip=None,user=None,site=None,mail_admins=False,callback=None):
        """
        Logs a message into site log
        """
        # Set IP value
        if ip is None:
            if not request is None:
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip=request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
                else:
                    ip=request.META['REMOTE_ADDR']
            else:
                ip='0.0.0.0'
                
        # Set user value
        if user is None:
            if not request is None:    
                if request.user.is_authenticated():
                    user=request.user
        
        # Set site value
        if site is None:
            if not request is None:
                site=get_site_from_request(request)
            else:
                site=Site.objects.get_current()
        # Check exceptions    
        if sys.exc_info() != (None,None,None):
            if data is not None:
                if isinstance(data, dict):
                    data['last_exception']=u'%s' % traceback.format_exc()
                else:
                    data.append(u'%s' % traceback.format_exc())
            else:
                data=[u'%s' % traceback.format_exc()]

        # Save log object
        if len(message) > 200:
            message=message[:200]
            data='%s\n%s' % (message,data)
        log=SiteLog(tag=tag,message=u'%s' % message,level=level,data=data,ip=ip,user=user,site=site)
        log.content_object=content_object
        log.save()
        
        # Mail admins if specified or needed
        if mail_admins or log.level <= settings.SITE_LOG_MAIL_ADMINS_LEVEL:
            body=render_to_string('sitelog/mail_admins.html', {'log': log})
            django_mail_admins(message,body,fail_silently=True)

        # Callback execution
        if callback is not None:
            return callback(log)

    def __unicode__(self):
        """
        Model unicode representation
        """
        return u'%s %s %s: %s' % (self.timestamp,self.get_level_display(),self.tag,self.message)

class LegalDocumentVersionManager(models.Manager):
    """
    Legal document version manager
    """
    def get_latest(self,document):
        """
        Get last document version
        """
        qs=self.get_queryset().filter(document=document).order_by('-date')
        if qs.count() > 0:
            return qs[0]
        return None

class LegalDocument(models.Model):
    """
    Legal document model
    """
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Legal document')
        verbose_name_plural=_('Legal documents')

    identifier=models.SlugField(_('Identifier'),unique=True,max_length=20,
        help_text=_('Legal document unique identifier'))
    name=models.CharField(_('Name'),max_length=100,
        help_text=_('Legal document name'))
    country=CountryField(_('Country'),blank=True,null=True,
        help_text=_('Country this legal document is intended for'))
    default=models.BooleanField(_('Default'),default=False,
        help_text=_('Default legal document'))
    desc=models.TextField(_('Description'),blank=True,null=True,
        help_text=_('Legal document description'))

    def get_latest(self):
        """
        Return latest version for this document
        """
        return LegalDocumentVersion.objects.get_latest(self)

    def get_version(self,version):
        """
        Return specific version for this document
        """
        return self.legaldocumentversion_set.get(version=version)
    
    @staticmethod
    def get_document_version(docid=None,version=None,country=None):
        """
        Get document version from given identifiers or default document latest version
        """
        if docid is not None:
    	    try:
	           document=LegalDocument.objects.get(identifier=docid,country=country)
            except:
	           return None
        else:
            try:
                document=LegalDocument.objects.get(default=True,country=country)
            except:
                return None
        if version is not None:
	       document=document.get_version(version)
        else:
	       document=document.get_latest()
        return document

    def __unicode__(self):
        """
        Model unicode representation
        """
        return self.name

class LegalDocumentVersion(models.Model):
    """
    Legal document version model
    """
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Legal document version')
        verbose_name_plural=_('Legal document versions')
        unique_together=('document','version')
    
    document=models.ForeignKey(LegalDocument,verbose_name=_('Legal document'),
        help_text=_('Legal document for this version'))
    lang=LanguageField(_('Language'),
        help_text=_('Legal document language for this version'))
    date=models.DateTimeField(_('Date'), 
        help_text=_('Date and time this document will apply'))
    version=models.CharField(_('Version'),max_length=20,
        help_text=_('Version number or identifier for this document'))
    content=models.TextField(_('Content'),
        help_text=_('Document content'))

    objects=LegalDocumentVersionManager()

    def accepted_by_user(self,user):
        """
        Check if this legal document version has been accepted by the user
        """
        acceptances=LegalDocumentAcceptance.objects.filter(documentversion=self,user=user)
        if acceptances.count() > 0:
            return acceptances[0]
        else:
            return None

    def __unicode__(self):
        """
        Model unicode representation
        """
        return u'%s %s' % (self.document.name,self.version)

class LegalDocumentAcceptance(models.Model):
    """
    Legal document acceptance by user accounts
    """
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Legal document acceptance')
        verbose_name_plural=_('Legal document acceptances')

    timestamp=models.DateTimeField(_('Timestamp'),auto_now_add=True,
        help_text=_('Date and time of document acceptance'))
    documentversion=models.ForeignKey(LegalDocumentVersion,verbose_name=_('Version'),
        help_text=_('Legal document version that has been accepted'))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('User'),blank=True,null=True,
        help_text=_('User that accepted terms'))
    desc=models.CharField(_('Description'),max_length=50,blank=True,null=True,
        help_text=_('Acceptance description'))
    ip=models.GenericIPAddressField(_('IP address'),blank=True,null=True,
        help_text=_('IP address from where the acceptance connection was made'))
    data=models.TextField(_('Data'),blank=True,null=True,
        help_text=_('Extra data for acceptance'))

    def __unicode__(self):
        """
        Model unicode representation
        """
        return u'%s: %s' % (self.user,self.documentversion)
