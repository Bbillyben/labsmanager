from django import forms
from .models import Employee, TeamMate
from django.contrib.auth.models import User
from django.db.models import Q

class TeamMateForm(forms.ModelForm):
    model = TeamMate
    fields = [
        "team",
        "employee",
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            teamMate= kwargs['instance']
            empInTeam = TeamMate.objects.filter(team=teamMate.team).values_list('employee')
            usersU =Employee.objects.filter(~Q(user__pk=teamMate.team.leader.user.pk))
            self.fields['employee'].queryset = usersU
        