# -*- coding: utf-8 -*-
"""
 Administration module
===============================================

.. module:: sitetools.admin
    :platform: Django
    :synopsis: administration module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.utils import flatten_fieldsets

# Application imports
from sitetools.models import SiteInfo
from sitetools.models import SiteLog
from sitetools.models import LegalDocument, LegalDocumentVersion, LegalDocumentAcceptance

class BaseModelAdminLogic(object):
    """
    Common logic for ModelAdmin classes
    """
    # Extra properties
    all_fields_readonly=False
    superuser_skips_all_readonly=True
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only
        """
        if not self.all_fields_readonly or (request.user.is_superuser and self.superuser_skips_all_readonly):
            return self.readonly_fields
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

class BaseModelAdmin(BaseModelAdminLogic,admin.ModelAdmin):
    """
    Base ModelAdmin administration class
    """
    save_on_top = True
    list_per_page = 50

class BaseTabularInline(BaseModelAdminLogic,admin.TabularInline):
    """
    Base TabularInline administration class
    """
    extra = 0

class BaseGenericTabularInline(BaseModelAdminLogic,GenericTabularInline):
    """
    Base Generic TabularInline administration class
    """
    extra = 0

class SiteInfoAdmin(BaseModelAdmin):
    """
    Administration class
    """
    # Admin parameters    
    list_display = ('site','active','maintenance')
    list_filter = ('active','maintenance')
    search_fields = ('site__domain','site__name')
    list_editable = ('active','maintenance')

class SiteLogInline(BaseGenericTabularInline):
    """
    Site log inline administration class
    """
    model = SiteLog

    def has_add_permission(self, request):
        return False

class SiteLogAdmin(admin.ModelAdmin):
    """
    Site log administration class
    """
    # Admin parameters    
    list_display = ('timestamp','tag','message','level','ip','user','content_type','object_id','admin_content_object')
    list_filter = ('timestamp','level','tag','user')
    search_fields = ('message','tag','user__username','user__first_name','user__last_name','ip','data')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def admin_content_object(self,obj):
        """
        Show content object unicode representation
        """
        try:
            if obj.content_object:
                return unicode(obj.content_object)
        except:
            pass
        return None
    admin_content_object.short_description=_('Content object')

class LegalDocumentVersionInline(BaseTabularInline):
    """
    Inline administration class
    """
    model = LegalDocumentVersion

class LegalDocumentAdmin(BaseModelAdmin):
    """
    Administration class
    """
    list_display = ('identifier','name','country',)
    list_filter = ('country',)
    search_fields = ('name','desc',)
    inlines = [LegalDocumentVersionInline,]

class LegalDocumentVersionAdmin(BaseModelAdmin):
    """
    Administration class
    """
    list_display = ('__unicode__','document','version','lang','date',)
    list_filter = ('document','date', 'lang',)
    search_fields = ('document__name', 'version',)

class LegalDocumentAcceptanceAdmin(BaseModelAdmin):
    """
    Administration class
    """
    search_fields = ('documentversion__document__name', 'documentversion__version','user__firstname','user__lastname','desc','data')
    list_display = ('__unicode__','timestamp','documentversion','user','desc')
    list_filter = ('timestamp','documentversion','user',)

# Admin models registration
admin.site.register(SiteInfo, SiteInfoAdmin)
admin.site.register(SiteLog, SiteLogAdmin)
admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(LegalDocumentVersion, LegalDocumentVersionAdmin)
admin.site.register(LegalDocumentAcceptance, LegalDocumentAcceptanceAdmin)
