# -*- coding: utf-8 -*-
"""
 Administration module
===============================================

.. module:: sitetools.admin
    :platform: Django
    :synopsis: administration module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import datetime

# Django imports
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.admin.filters import FieldListFilter
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.contenttypes.admin import GenericTabularInline
from django.conf import settings

# Application imports
from sitetools.models import SiteInfo, SiteLog, SiteVar
from sitetools.models import LegalDocument, LegalDocumentVersion, LegalDocumentAcceptance

class EnhancedDateFieldListFilter(FieldListFilter):
    """
    Modified original django date filter to allow future dates
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_generic = '%s__' % field_path
        self.date_params = dict([(k, v) for k, v in params.items()
                                 if k.startswith(self.field_generic)])

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        
        # Calculate months
        onemonthlater=today.month+1
        if onemonthlater > 12:
            onemonthlater=1
        twomonthslater=onemonthlater+1
        if twomonthslater > 12:
            twomonthslater =1
        
        self.links = (
            (_('Any date'), {}),
            (_('This year'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 30 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=30)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 15 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=15)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 7 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Yesterday'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=1)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Tomorrow'), {
                self.lookup_kwarg_since: str(tomorrow),
                self.lookup_kwarg_until: str(tomorrow + datetime.timedelta(days=1)),
            }),
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
            (_('Next 15 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=15)),
            }),
            (_('Next 30 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=30)),
            }),
            (_('Next month'), {
                self.lookup_kwarg_since: str(today.replace(day=1,month=onemonthlater)),
                self.lookup_kwarg_until: str(today.replace(day=1,month=twomonthslater)),
            }),
            (_('Next year'), {
                self.lookup_kwarg_since: str(today.replace(day=1,month=1,year=today.year+1)),
                self.lookup_kwarg_until: str(today.replace(day=1,month=1,year=today.year+2)),
            }),
        )
        super(EnhancedDateFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_until]

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {
                'selected': self.date_params == param_dict,
                'query_string': cl.get_query_string(
                                    param_dict, [self.field_generic]),
                'display': title,
            }

class AdminImageFileWidget(AdminFileWidget):
    """
    Custom administration system widget for image fields
    """
    def render(self, name, value, attrs=None):
        """
        HTML Rendering
        """
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            output.append('<a target="_blank" href="%s"><img src="%s" height="100"/></a><br /><a target="_blank" href="%s">%s</a><br /> ' % \
                (file_path, file_path, _('Currently:'), _('Change:')))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

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


class SiteVarInline(BaseTabularInline):
    """
    Site log inline administration class
    """
    model = SiteVar

class SiteInfoAdmin(BaseModelAdmin):
    """
    Administration class
    """
    # Admin parameters    
    list_display = ('site','active','maintenance')
    list_filter = ('active','maintenance')
    search_fields = ('site__domain','site__name')
    list_editable = ('active','maintenance')
    inlines = [SiteVarInline,]

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
    list_display = ('__unicode__','timestamp','documentversion','user','desc')
    list_filter = ('timestamp','documentversion','user',)
    search_fields = ('documentversion__document__name','documentversion__version','user__first_name','user__last_name','desc','data',)

# Admin models registration
admin.site.register(SiteInfo, SiteInfoAdmin)
admin.site.register(SiteLog, SiteLogAdmin)
admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(LegalDocumentVersion, LegalDocumentVersionAdmin)
admin.site.register(LegalDocumentAcceptance, LegalDocumentAcceptanceAdmin)

# Register enhanced field filters
FieldListFilter.register(
    lambda f: isinstance(f, models.DateField), EnhancedDateFieldListFilter,take_priority=True)