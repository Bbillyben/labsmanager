
from .models import Milestones
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from project.models import Project
from labsmanager.forms import DateInput

from labsmanager.mixin import SanitizeDataFormMixin

class MilestonesModelForm(SanitizeDataFormMixin, BSModalModelForm):
    class Meta:
        model = Milestones
        fields = ['project', 'name','desc','deadline_date', 'type', 'quotity', 'status',]
        widgets = {
            'deadline_date': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'project' in kwargs['initial']):
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=Project.objects.all(),
                widget=forms.HiddenInput
            )
            proj = Project.objects.get(pk=kwargs['initial']['project'])
        else:
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=Project.objects.all(),
            )
            
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['project'].widget = forms.HiddenInput()