from pyexpat import model
from statistics import mode
from django.db import models
from django.utils.translation import gettext_lazy as _
from fund.models import Fund, Cost_Type
from staff.models import Employee
from django.db.models import Q, Sum

from labsmanager.models_utils import PERCENTAGE_VALIDATOR    


# Create your models here.
class Expense(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Expense")
        
    date = models.DateField(null=False, blank=False, verbose_name=_('Expense Date'))
    type = models.ForeignKey(Cost_Type, on_delete=models.CASCADE, verbose_name=_('Type'))
    amount=models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'))
    status_mod=(("e",_("Engaged")), 
                ("r", _("Realised")),
                ("p", _("Projected")),
                )
    status= models.CharField(
        max_length=1,
        choices=status_mod,
        blank=False,
        default='e', verbose_name=_('Status'),
    )
    fund_item = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name=_('Related Fund'))
    
    def __str__(self):
        return f'{self.fund_item.__str__()}/{self.type}: {self.amount} ({self.status})'


class Contract_expense(Expense):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Contract Expense")
    contract= models.ForeignKey('Contract', on_delete=models.CASCADE, verbose_name=_('Related Contract'))


class Contract_type(models.Model):
    class Meta:
        verbose_name = _("Contract Type")
    name = models.CharField(max_length=60, verbose_name=_('Type name'))
    
    def __str__(self):
        return f'{self.name}'
    
class Contract(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Contract")
        
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    start_date=models.DateField(null=True, blank=True, verbose_name=_('Contract Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('Contract End Date'))
    quotity = models.DecimalField(max_digits=4, decimal_places=3, default=0, validators=PERCENTAGE_VALIDATOR, verbose_name=_('Time qutotity'))
    fund=models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name=_('Related Fund'))
    contract_type=models.ForeignKey(Contract_type,null=True, on_delete=models.SET_NULL, verbose_name=_('Contract Type'))
    
    def __str__(self):
        return f'{self.employee.__str__()} - {self.fund.__str__()}'
    
    @property
    def total_amount(self):
        exp = Contract_expense.objects.filter(contract=self.pk)
        if exp:
            return exp.aggregate(Sum('amount'))["amount__sum"]
        return 0