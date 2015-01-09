#-------------------------------------------------------------------------------
# Forms
#-------------------------------------------------------------------------------

# Django imports
from django import forms
from django.utils.translation import ugettext,ugettext_lazy as _
from django.conf import settings

# Site tools imports
from sitetools.forms.fields import EULAField, RECAPTCHAField
from sitetools.models import ContactMessage

class ContactForm(forms.ModelForm):
    """
    Contact form
    """
    # Form metadata
    class Meta:
        model=ContactMessage
        fields=('name','email','text','eula','captcha')

    # Form fields
    # TODO: Change EULA URL
    eula=EULAField(eula_url='/legal/')
    captcha=RECAPTCHAField(label=_('Verification code'))