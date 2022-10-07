from time import altzone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Employee(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Employee")
        verbose_name_plural = _("Employee")

    """Model for employee"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)
    

    
    def __str__(self):
        """Return a string representation of the Employee (for use in the admin interface)"""
        return  f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
    
class Employee_Status(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Status")
        verbose_name_plural = _("Status")
        
        
    type = models.ForeignKey('Employee_type', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.employee.user.first_name} {self.employee.user.last_name}  : {self.type.name}"
    
    
class Employee_Type(models.Model):
    
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Employee Type")
        
    shortname = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.name} ({self.shortname})"

class Team(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Team")
    
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE)

class TeamMate(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("TeamMate")    
        
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)