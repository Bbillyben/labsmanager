from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


from faicon.fields import FAIconField
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

####################### GENERAL Informations #################
######  informations about institution or funder
## 1 type / icon + name
## 2 info with generic foreign key
class InfoTypeClass(models.Model):
    class Meta:
        abstract = True
        ordering = ['name']
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    icon = FAIconField(null=True,)
    type_choices=[("none",_("None")), ("tel",_("Phone Number")), ("mail", _("EMail")), ("link", _("Link")), ("addr", _("Address")),]
    type = models.CharField(
        max_length=4,
        choices=type_choices,
        blank=False,
        default=type_choices[0][0], 
        verbose_name=_('Type'),        
    )
    
    def __str__(self):
       return self.name
    

class OrganizationInfosType(InfoTypeClass):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Type of Organization Info")
        ordering = ['name']
    

    
    

class OrganizationInfos(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Organization Info")
    
    #orga = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    content_type = models.ForeignKey(ContentType, related_name="content_type_oragnization", on_delete=models.CASCADE, )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    info =  models.ForeignKey(OrganizationInfosType, on_delete=models.CASCADE, verbose_name=_('Info Type'))
    value = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Info Value'))
    comment = models.TextField(max_length=350, blank=True, null=True, verbose_name=_('comment'))
    history = AuditlogHistoryField()

    def __str__(self):
       return f'{self.info.name} - {self.value}'
    
    
########################## CONTACT ##########################
##### Contact for insitution or funder
## 1 type of contact
## 2 contact with foregin key + free comment

##### Contact information 
## 1 type of information (eg tel, mail, ) / icon + name
## 2 infos / contact + type + value


class ContactType(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Type of Contact")
        ordering = ['name']
    
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    
    def __str__(self):
       return self.name

class ContactInfoType(InfoTypeClass):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Type of Contact Info")
        ordering = ['name']



class Contact(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Organization's Contact")
        
        
    content_type = models.ForeignKey(ContentType, related_name="content_type_contact", on_delete=models.CASCADE, )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))  
    type =  models.ForeignKey(ContactType, on_delete=models.CASCADE, verbose_name=_('Contact Type'))
    comment = models.TextField(max_length=350, blank=True, null=True, verbose_name=_('comment'))
    history = AuditlogHistoryField()

    def __str__(self):
       return f'{self.first_name} {self.last_name} - {self.content_object}'

class ContactInfo(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Contact Info")

    contact =  models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name=_('Contact'))
    info =  models.ForeignKey(ContactInfoType, on_delete=models.CASCADE, verbose_name=_('Contact Info Type'))
    value = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Info Value'))
    comment = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('comment'))
    
    def __str__(self):
       return f'{self.contact.first_name} {self.contact.last_name} - {self.info.name}'
   
   
   
# =================   Generic Note  on everything   ================= #
# =================================================================== #
# add information to an object (project, employee, institution, .. can be extended)
# pip install django-markdownfield for markdown field ?

from labsmanager.mixin import TimeStampMixin
from common.nh3_fields import Nh3Field_CharField, Nh3Field_TextField
import nh3
from django_prose_editor.sanitized import SanitizedProseEditorField
class GenericNote(TimeStampMixin):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Generic Notes")
        unique_together = ('content_type', 'object_id', 'name')
        ordering = ["created_at"]
        
    content_type = models.ForeignKey(ContentType, related_name="content_type_note", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    name = Nh3Field_CharField(
        max_length=50, verbose_name=_('Name'), default=_('General'))
    note=SanitizedProseEditorField(
                    config = {
                        "types": None,        # Allow all nodes and marks
                        "history": True,      # Enable undo and redo
                        "html": True,         # Add a button which allows editing the raw HTML
                        "typographic": True,  # Highlight typographic characters
                    }, 
                    blank=True,
                    verbose_name=_('note')                    
            )
    
    def __str__(self):
       return f'{self.name} {self.content_type} - {self.content_object}'
    
    
auditlog.register(OrganizationInfos)
auditlog.register(Contact)
auditlog.register(GenericNote)