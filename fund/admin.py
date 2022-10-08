from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from fund.models import Cost_Type, Fund_Institution, Fund_Item, Fund


class CostTypeAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')

class FundTypeInline(admin.TabularInline):
    model=Fund_Item
    extra=0

class FundAdmin(admin.ModelAdmin):
    list_display = ('get_proj_name','get_funder_name','get_manager_name', 'ref',)
    inlines = [FundTypeInline]
    
    def get_proj_name(self, obj):
        return obj.project.name
    get_proj_name.short_description = _('Project')
    get_proj_name.admin_order_field = 'fund__project_name'
    
    def get_funder_name(self, obj):
        return obj.funder.short_name
    get_funder_name.short_description = _('Funder')
    get_funder_name.admin_order_field = 'fund__funder_name'
    
    def get_manager_name(self, obj):
        return obj.institution.short_name
    get_manager_name.short_description = _('Manager')
    get_manager_name.admin_order_field = 'fund__manager_name'
    
# Register your models here.
admin.site.register(Cost_Type, CostTypeAdmin)
admin.site.register(Fund_Institution, CostTypeAdmin)
admin.site.register(Fund, FundAdmin)