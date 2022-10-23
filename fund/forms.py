from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError
from . import models
from project.models import Project
from django.utils.translation import gettext_lazy as _
from django import forms


class FundItemModelForm(BSModalModelForm):
    class Meta:
        model = models.Fund_Item
        fields = ['fund', 'type','amount',]

    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'fund' in kwargs['initial']):
            self.base_fields['fund'] = forms.ModelChoiceField(
                queryset=models.Fund.objects.all(),
                widget=forms.HiddenInput
            )
        else:
            self.base_fields['fund'] = forms.ModelChoiceField(
                queryset=models.Fund.objects.all(),
            )
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['fund'].widget = forms.HiddenInput()
            
            
class FundModelForm(BSModalModelForm):
    class Meta:
        model = models.Fund
        fields = ['project', 'funder','institution','start_date', 'end_date', 'ref',]

    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'project' in kwargs['initial']):
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=models.Project.objects.all(),
                widget=forms.HiddenInput
            )
        else:
            self.base_fields['project'] = forms.ModelChoiceField(
                queryset=models.Project.objects.all(),
            )
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['funder'].widget = forms.HiddenInput()
            self.fields['institution'].widget = forms.HiddenInput()
            
    def clean_end_date(self):
        print("EXIT DATE CLEAN Fund Model :"+str(self.cleaned_data))
        if( self.cleaned_data['end_date'] != None and (self.cleaned_data['start_date'] == None or self.cleaned_data['start_date'] > self.cleaned_data['end_date'])):
            raise ValidationError(_('Exit Date (%s) should be later than entry date (%s) ') % (self.cleaned_data['end_date'], self.cleaned_data['start_date']))
        return self.cleaned_data['end_date']