from secrets import choice
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError
from . import models
from django.utils.translation import gettext_lazy as _
from django import forms
from staff.models import Employee

from labsmanager.forms import DateInput

class ProjectModelForm(BSModalModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'start_date', 'end_date','status',]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProjectModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].disabled = True
            
    def clean_end_date(self):
        if( self.cleaned_data['end_date'] != None and (self.cleaned_data['start_date'] == None or self.cleaned_data['start_date'] > self.cleaned_data['end_date'])):
            raise ValidationError(_('Exit Date (%(end)s) should be later than entry date (%(start)s) ') % ({'end':self.cleaned_data['end_date'], 'start': self.cleaned_data['start_date']}))
        return self.cleaned_data['end_date']

class ParticipantModelForm(BSModalModelForm):
    class Meta:
        model = models.Participant
        fields = ['project', 'employee','status','start_date', 'end_date', 'quotity',]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        
    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'project' in kwargs['initial']):
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=models.Project.objects.all(),
                widget=forms.HiddenInput
            )
            proj = models.Project.objects.get(pk=kwargs['initial']['project'])
            if proj:
                self.base_fields['start_date'].initial = proj.start_date
                self.base_fields['end_date'].initial = proj.end_date
        else:
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=models.Project.objects.all(),
            )
        if ('initial' in kwargs and 'employee' in kwargs['initial']):
            self.base_fields['employee'] = forms.ModelChoiceField(
                queryset=Employee.objects.all(),
                widget=forms.HiddenInput
            )
        else:
            self.base_fields['employee'] = forms.ModelChoiceField(
                queryset=Employee.objects.filter(is_active=True),
            )
            
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['employee'].widget = forms.HiddenInput()
            self.fields['project'].widget = forms.HiddenInput()
        
        
            
    def clean_end_date(self):
        if( self.cleaned_data['end_date'] != None and (self.cleaned_data['start_date'] == None or self.cleaned_data['start_date'] > self.cleaned_data['end_date'])):
            raise ValidationError(_('Exit Date (%(end)s) should be later than entry date (%(start)s) ') % ({'end':self.cleaned_data['end_date'], 'start': self.cleaned_data['start_date']}))
        return self.cleaned_data['end_date']

class InstitutionModelForm(BSModalModelForm):
    class Meta:
        model = models.Institution_Participant
        fields = ['project', 'institution','status',]
        
    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'project' in kwargs['initial']):
            self.base_fields['project'].widget= forms.HiddenInput()
            # proj = models.Project.objects.get(pk=kwargs['initial']['project'])
            # if proj:
            #     self.base_fields['start_date'].initial = proj.start_date
            #     self.base_fields['end_date'].initial = proj.end_date
        else:
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=models.Project.objects.all(),
            )
        if ('initial' in kwargs and 'institution' in kwargs['initial']):
            self.base_fields['institution'].widget= forms.HiddenInput()
        else:
            self.base_fields['institution'] = forms.ModelChoiceField(
                queryset=models.Institution.objects.all(),
            )
            
        super().__init__(*args, **kwargs)
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     self.fields['employee'].widget = forms.HiddenInput()
        #     self.fields['project'].widget = forms.HiddenInput()
class InstitutionModelFormDirect(BSModalModelForm):
    class Meta:
        model = models.Institution
        fields = ['name','short_name','adress',]
        
class GenericInfoProjectForm(BSModalModelForm):
    class Meta:
        model = models.GenericInfoProject
        fields = ['info', 'project', 'value',]
    
    def __init__(self, *args, **kwargs): 
        
        self.base_fields['project'] = forms.ModelChoiceField(
            queryset=models.Project.objects.all(),
            widget=forms.HiddenInput
        )
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['info'].disabled = True
            
class GenericInfoTypeProjectForm(BSModalModelForm):
    class Meta:
        model = models.GenericInfoTypeProject
        fields = ['name', 'icon',]

    @property
    def media(self):
        response = super().media
        response._js_lists.clear()
        response._js_lists.append(['js/faicon_in/list.min.js'])
        response._js_lists.append(['js/faicon_in/faicon.js'])
        return response