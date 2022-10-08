from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from project.models import Project, Institution


class Cost_Type(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Cost Type")
        
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
        
        
    type=models.ForeignKey(Cost_Type, on_delete=models.CASCADE, verbose_name=_('Type'))
    amount=models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'))
    fund=models.ForeignKey('Fund', on_delete=models.CASCADE, verbose_name=_('Related Fund'))

class Fund(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Fund"
                         )
    project=models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Funded Project'))
    funder=models.ForeignKey(Fund_Institution, on_delete=models.CASCADE, verbose_name=_('Fund Instituition'))
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name=_('Manager Institution'))
    
    ref= models.CharField(max_length=30, blank=True, verbose_name=_('Reference'))
    
    def __str__(self):
        return f'{self.project.name} | {self.funder.short_name} -> {self.institution.short_name}'