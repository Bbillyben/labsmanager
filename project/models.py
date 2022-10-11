from django.db import models
from django.utils.translation import gettext_lazy as _

class Institution(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Lab Institution")
        
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
        
    name = models.CharField(max_length=50, verbose_name=_('Project Name'), unique=True)
    start_date=models.DateField(null=False, blank=False, verbose_name=_('Start Date'))
    end_date=models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    status=models.BooleanField(default=True, verbose_name=_('Project Status'))
    
    def get_status(self):
        return self.status
    get_status.boolean = True
    
    def __str__(self):
        """Return a string representation of the Status (for use in the admin interface)"""
        return f"{self.name}"
    
class Institution_Participant(models.Model):
    class Meta:
        """Metaclass defines extra model properties"""
        verbose_name = _("Partner Institution")
        
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