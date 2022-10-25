from django.contrib import admin
from expense.models import Expense, Contract_expense, Contract, Contract_type
from fund.models import Fund
from django.utils.translation import gettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django import forms
from functools import partialmethod, partial
    
class ContractExpenseInlineFormSet(BaseInlineFormSet):
    
    def __init__(self, *args, **kwargs):
        print(" ================= Init ContractExpenseInlineFormSet  ===================== ")
        print('kwargs : '+str(kwargs))
        super().__init__(*args, **kwargs)
        if 'instance' in  kwargs:
            instance = kwargs['instance']
            print('fund id  : '+str(instance.fund.pk))
            for form in self.forms:
                form.fields['fund_item'] =forms.ModelChoiceField(
                    queryset=Fund.objects.filter(pk=instance.fund.pk),
                    initial=instance.fund,
                )
            print(" ->"+str(self.forms))

    
class Contract_expenseInline(admin.TabularInline):
    model=Contract_expense
    extra=0
    formset = ContractExpenseInlineFormSet
    fields =['date', 'type', 'amount', 'status','fund_item']
    # exclude = ['fund_item']   

    # def get_formset(self, request, obj=None, **kwargs):
        
    #     initial = []
    #     if request.method == "GET":
    #         initial.append({
    #             'fund_item': obj.fund.pk,
    #         })
    #         print("get_formset : "+str(obj.fund.pk))
    #         kwargs['initial']=initial
    #     formset = super(Contract_expenseInline, self).get_formset(request, obj, **kwargs)
    #     #formset.__init__ = partial(formset.__init__, obj, **kwargs)
    #     return formset
    
class ContractAdmin(admin.ModelAdmin):
    list_display = ('__str__','get_proj_name','get_fund_name', 'start_date', 'end_date', 'quotity')
    inlines = [Contract_expenseInline,]
     
    def get_proj_name(self, obj):
        return obj.fund.project.__str__()
    get_proj_name.short_description = _('Project')
    get_proj_name.admin_order_field = 'project__name'
    
    
    def get_fund_name(self, obj):
        return obj.fund.funder.__str__()
    get_fund_name.short_description = _('Funder')
    get_fund_name.admin_order_field = 'funder__short_name'
    

# Register your models here.
admin.site.register(Expense)
admin.site.register(Contract_expense)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Contract_type)