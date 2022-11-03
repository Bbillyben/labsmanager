from django.contrib import admin
from staff.models import Employee, Employee_Status, Employee_Type, Team, TeamMate
from django.utils.translation import gettext_lazy as _
from .forms import TeamMateForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin


# ressource for import export 
class EmployeeResource(resources.ModelResource):
    

    class Meta:
        model = Employee
        skip_unchanged = True
        report_skipped = True
        
        fields = ('id', 'first_name', 'last_name', 'birth_date','entry_date', 'exit_date', 'is_active',)
        
        
# admin class
class EmployeeStatusInline(admin.TabularInline):
    model = Employee_Status
    extra = 0
    
    
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name',  'entry_date' , 'exit_date', 'is_active', 'get_user')
    fieldsets = (
        ('Employee', {
            'fields': ('first_name', 'last_name', 'birth_date')
        }),
        ('Lab Status', {
            'fields': ('entry_date', 'exit_date', 'is_active')
        }),
        ('LabsManager User', {
            'fields': ('user',)
        }),
    )
    inlines = [EmployeeStatusInline]
    list_filter=('entry_date' , 'exit_date')
    resource_classes = [EmployeeResource]
     
    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return None
    get_user.short_description = _('User Attached')
    get_user.admin_order_field = 'user_attached'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = _('First Name')
    get_first_name.admin_order_field = 'user__first_name'
    
    
class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname' )

# For Team Admin
class TeamMateInline(admin.TabularInline):
    model = TeamMate
    extra=0
    #form = TeamMateForm
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader' )
    inlines = [TeamMateInline]
    
    

     
# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(Employee_Status)
admin.site.register(Employee_Type, EmployeeTypeAdmin)

admin.site.register(Team, TeamAdmin)
admin.site.register(Employee_Status)