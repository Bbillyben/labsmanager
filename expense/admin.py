from django.contrib import admin
from expense.models import Expense, Contract_expense, Contract
from django.utils.translation import gettext_lazy as _


class ContractAdmin(admin.ModelAdmin):
    list_display = ('__str__','get_proj_name','get_fund_name', 'start_date', 'end_date', 'quotity')
    
    
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