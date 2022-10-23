from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.utils import is_ajax
from django.core.exceptions import ValidationError
from . import models
from staff.models import Employee
from django.utils.translation import gettext_lazy as _
from django import forms
from fund.models import Cost_Type, Fund

class ContractModelForm(BSModalModelForm):
    class Meta:
        model = models.Contract
        fields = ['employee', 'fund','start_date','end_date', 'quotity',]

    def __init__(self, *args, **kwargs):
        if ('initial' in kwargs and 'employee' in kwargs['initial']):
            self.base_fields['employee'] = forms.ModelChoiceField(
                queryset=Employee.objects.all(),
                widget=forms.HiddenInput
            )
        else:
            self.base_fields['employee'] = forms.ModelChoiceField(
                queryset=Employee.objects.all(),
            )
        
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['employee'].widget = forms.HiddenInput()
            self.fields['fund'].widget = forms.HiddenInput()

    def clean_end_date(self):
        print("EXIT DATE CLEAN Fund Model :"+str(self.cleaned_data))
        if( self.cleaned_data['end_date'] != None and (self.cleaned_data['start_date'] == None or self.cleaned_data['start_date'] > self.cleaned_data['end_date'])):
            raise ValidationError(_('Exit Date (%s) should be later than entry date (%s) ') % (self.cleaned_data['end_date'], self.cleaned_data['start_date']))
        return self.cleaned_data['end_date']
    
class ContractExpenseModelForm(BSModalModelForm):
    class Meta:
        model = models.Contract_expense
        fields = ['contract', 'date', 'type','status','amount',]

    def __init__(self, *args, **kwargs):
        self.base_fields['type'].queryset = Cost_Type.objects.filter(short_name__startswith='RH')
        if ('initial' in kwargs and 'contract' in kwargs['initial']):
            self.base_fields['contract'] = forms.ModelChoiceField(
                queryset=models.Contract.objects.all(),
                widget=forms.HiddenInput
            )
        else:
            self.base_fields['contract'] = forms.ModelChoiceField(
                queryset=models.Contract.objects.all(),
            )
        
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['contract'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
        if not is_ajax(self.request.META) or self.request.POST.get('asyncUpdate') == 'True':
            instance = super(ContractExpenseModelForm, self).save(commit=False)
            cont=instance.contract
            instance.fund_item = cont.fund
            if commit:
                instance.save()
        else:
            instance = super(ContractExpenseModelForm, self).save(commit=False)
        return instance
    