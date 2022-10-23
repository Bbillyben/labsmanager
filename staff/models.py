from time import altzone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Sum


### Models 
class Employee(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Employee")
        verbose_name_plural = _("Employee")

    """Model for employee"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth Date'))
    entry_date = models.DateField(null=True, blank=True, verbose_name=_('Entry Date'))
    exit_date = models.DateField(null=True, blank=True, verbose_name=_('Exit Date'))
    
    @property
    def user_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def is_team_leader(self):
        teams=Team.objects.filter(leader=self.pk)
        if teams:
            return True
        return False
    
    @property
    def is_team_mate(self):
        teams=TeamMate.objects.filter(employee=self.pk)
        if teams:
            return True
        return False
    
    @property
    def is_active(self):
        return self.user.is_active
    
    @property
    def get_status(self):
        return Employee_Status.objects.filter(employee=self.pk)
    
    @property
    def contracts(self):
        from expense.models import Contract
        return Contract.objects.filter(employee=self.pk)
    
    #ItemPrice.objects.aggregate(Sum('price'))
    @property
    def contracts_quotity(self):
        from expense.models import Contract
        return Contract.objects.filter(employee=self.pk, end_date=None).aggregate(Sum('quotity'))["quotity__sum"]

    @property
    def projects(self):
        from project.models import Participant
        return Participant.objects.filter(employee=self.pk)
    
    @property
    def projects_quotity(self):
        from project.models import Participant
        return Participant.objects.filter(employee=self.pk).aggregate(Sum('quotity'))["quotity__sum"]
    
    def __str__(self):
        """Return a string representation of the Employee (for use in the admin interface)"""
        return  f"{self.user.first_name} {self.user.last_name} ({self.user.username})"




class Employee_Status(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Status")
        verbose_name_plural = _("Status")
        
        
    type = models.ForeignKey('Employee_type', on_delete=models.CASCADE, verbose_name=_('Type'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    start_date=models.DateField(null=True, blank=True, verbose_name=_('Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.employee.user.first_name} {self.employee.user.last_name}  : {self.type.name}"
    

class Employee_Type(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Employee Type")
        
    shortname = models.CharField(max_length=10, verbose_name=_('Abbreviation'), unique=True)
    name = models.CharField(max_length=50, verbose_name=_('Name'), unique=True)
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.name} ({self.shortname})"

class Team(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Team")
    
    name = models.CharField(max_length=50, verbose_name=_('Team Name'))
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Team Leader'))
    
    @property
    def nb_mate(self):
        mates = TeamMate.objects.filter(team=self.pk)
        if mates: return mates.count()
        return 0
    
    @property
    def team_mate(self):
        return TeamMate.objects.filter(team=self.pk)
        
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.name}"

class TeamMate(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("TeamMate")    
        
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_('Team'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.team} / {self.employee}"
    
    def clean(self):
        team = self.team
        inuser = TeamMate.objects.filter(Q(employee=self.employee), Q(team=team), ~Q(pk=self.pk))
        if inuser:
            raise ValidationError(_('Already in Team'))
        isLeader = Team.objects.filter(Q(pk=self.team.pk), Q(leader=self.employee))
        print(isLeader)
        if isLeader:
            raise ValidationError(_('Is Team leader'))
        