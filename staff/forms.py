from csv import field_size_limit
from traceback import format_tb
from django import forms
from .models import Employee, TeamMate, Employee_Status
from django.contrib.auth.models import User
from django.db.models import Q
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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


class EmployeeModelForm(BSModalModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'birth_date', 'entry_date', 'exit_date']
        
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].disabled = True
            
    def clean_exit_date(self):
        # print("EXIT DATE CLEAN"+str(self.cleaned_data))
        if( self.cleaned_data['exit_date'] != None and self.cleaned_data['entry_date'] > self.cleaned_data['exit_date']):
            raise ValidationError(_('Exit Date (%s) should be later than entry date (%s) ') % (self.cleaned_data['exit_date'], self.cleaned_data['entry_date']))
        return self.cleaned_data['exit_date']

class EmployeeStatusForm(BSModalModelForm):
    class Meta:
        model = Employee_Status
        fields = ['type', 'start_date', 'end_date', 'employee']
    
    def __init__(self, *args, **kwargs): 
        
        self.base_fields['employee'] = forms.ModelChoiceField(
            queryset=Employee.objects.all(),
            widget=forms.HiddenInput
        )
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['type'].disabled = True
    
    def clean_end_date(self):
        # print("End DATE CLEAN"+str(self.cleaned_data))
        if( self.cleaned_data['end_date'] != None and (self.cleaned_data['start_date'] == None or self.cleaned_data['start_date'] > self.cleaned_data['end_date'])):
            raise ValidationError(_('End Date (%s) should be later than start date (%s) ') % (self.cleaned_data['end_date'], self.cleaned_data['start_date']))
        return self.cleaned_data['end_date']