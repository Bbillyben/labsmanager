from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from staff.models import Employee
from labsmanager.models_utils import PERCENTAGE_VALIDATOR 
from datetime import date
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from settings.models import LMUserSetting
from dashboard import utils
class Institution(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Lab Institution")
        ordering = ['short_name']
        
    """List of institution public"""
    short_name= models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150, unique=True)
    adress=models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.short_name}"
    
class Project(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("project")
        ordering = ['name']
    name = models.CharField(max_length=50, verbose_name=_('Project Name'), unique=True)
    start_date=models.DateField(null=False, blank=False, verbose_name=_('Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    status=models.BooleanField(default=True, verbose_name=_('Project Status'))
    history = AuditlogHistoryField()
    
    def get_status(self):
        return self.status
    get_status.boolean = True
    
    @property
    def get_funds_amount(self):
        from fund.models import Fund, Fund_Item
        fundP=Fund.objects.filter(project=self.pk).only('pk').all()
        return Fund_Item.objects.filter(fund__in = fundP).only('amount').aggregate(Sum('amount'))["amount__sum"]
    
    @property
    def get_total_participant_quotity(self):
        parti=Participant.objects.filter(Q(project=self.pk) & (Q(end_date=None) | Q(end_date__gte=date.today()))).only('quotity')
        return parti.aggregate(Sum('quotity'))["quotity__sum"]
    
    @property
    def get_total_contract_quotity(self):
        from expense.models import Contract
        from fund.models import Fund, Fund_Item
        fundP=Fund.objects.filter(project=self.pk).only('pk').all()
        cont=Contract.objects.filter(Q(fund__in = fundP) & (Q(end_date=None) | Q(end_date__gte=date.today()))).only('quotity')
        return cont.aggregate(Sum('quotity'))["quotity__sum"]   
    
    @classmethod
    def staleFilter(cls):
        monthToGo=LMUserSetting.get_setting('DASHBOARD_PROJECT_STALE_TO_MONTH')
        maxDate=utils.getDateToStale(monthToGo)
        return (Q(status=True) & Q(end_date__lte=maxDate))
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.name}"
    
class Institution_Participant(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Partner Institution")
        unique_together = ('project', 'institution',)
        
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name=_('Institution'))
    type_part=(("c",_("Coordinator")), ("p", _("Participant")))
    status = models.CharField(
        max_length=1,
        choices=type_part,
        blank=False,
        default='p', 
        verbose_name=_('Status'),        
    )
    history = AuditlogHistoryField()

class Participant(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    employee =  models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    start_date=models.DateField(null=False, blank=False, verbose_name=_('Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    type_part=(("l",_("Leader")), ("cl", _("Co Leader")), ("p", _("Participant")))
    status = models.CharField(
        max_length=2,
        choices=type_part,
        blank=False,
        default='p', 
        verbose_name=_('Status'),        
    )
    quotity = models.DecimalField(max_digits=4, decimal_places=3, default=0, validators=PERCENTAGE_VALIDATOR, verbose_name=_('Time qutotity'))
    history = AuditlogHistoryField()
    
    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
    
    # def project_name(self):
    #     return self.project.name
    
    # def project_status(self):
    #     return self.project.status
    
    def clean(self):
        project = self.project
        ## user already in team withou end date
        inuser = Participant.objects.filter(Q(employee=self.employee), Q(project=project), ~Q(pk=self.pk), Q(end_date=None))
        if inuser:
            raise ValidationError(_('Already in Team'))
        # user already in but has finished but date between
        q = (Q(start_date__lte=self.start_date) & Q(end_date__gte=self.start_date))
        if self.end_date:
            q= q | (Q(start_date__lte=self.end_date) & Q(end_date__gte=self.end_date))
        
        inuser = Participant.objects.filter(Q(employee=self.employee), Q(project=project), ~Q(pk=self.pk),
                                            
                                           q
                                            
                                            )
        if inuser:
            raise ValidationError(_('Already in Team At That Date'))


    def __str__(self):
        return self.employee.__str__()

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
    
auditlog.register(Project)
auditlog.register(Institution_Participant)
auditlog.register(Participant)