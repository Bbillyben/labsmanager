from tabnanny import verbose
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from project.models import Project, Institution

from mptt.models import MPTTModel, TreeForeignKey

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

class Cost_Type(MPTTModel):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Cost Type")
    
    class MPTTMeta:
        order_insertion_by = ['name']
                
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    short_name= models.CharField(max_length=10, verbose_name=_('Abbreviation'))
    name = models.CharField(max_length=60, verbose_name=_('Type name'))
    
    def __str__(self):
        return f'{self.name}'
    
class Fund_Institution(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Funder Institution")
        
    short_name= models.CharField(max_length=10, verbose_name=_('Funder abbreviation'))
    name = models.CharField(max_length=60, verbose_name=_('Funder Name'))
    
    def __str__(self):
        return f'{self.short_name}'
    
class Fund_Item(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Fund Line")
        unique_together = ('type', 'fund',)
        
    type=models.ForeignKey(Cost_Type, on_delete=models.CASCADE, verbose_name=_('Type'))
    amount=models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'))
    fund=models.ForeignKey('Fund', on_delete=models.CASCADE, verbose_name=_('Related Fund'))
    history = AuditlogHistoryField()

class Fund(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Fund")
    project=models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Funded Project'))
    funder=models.ForeignKey(Fund_Institution, on_delete=models.CASCADE, verbose_name=_('Fund Instituition'))
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name=_('Manager Institution'))
    start_date=models.DateField(null=False, blank=False, verbose_name=_('Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    ref= models.CharField(max_length=30, blank=True, verbose_name=_('Reference'))
    history = AuditlogHistoryField()
    
    def clean_end_date(self):
        ## print("EXIT DATE CLEAN Fund Model :"+str(self.cleaned_data))
        if( self.end_date != None and (self.start_date == None or self.start_date > self.end_date)):
            raise ValidationError(_('Exit Date (%s) should be later than entry date (%s) ') % (self.end_date, self.start_date))
        return self.end_date
    
    def __str__(self):
        return f'{self.project.name} | {self.funder.short_name} -> {self.institution.short_name}'
    
auditlog.register(Fund_Item)
auditlog.register(Fund)