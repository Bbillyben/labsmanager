from django.contrib import admin
from staff.models import Employee, Employee_Status, Employee_Type, Team, TeamMate

class EmployeeStatusInline(admin.TabularInline):
    model = Employee_Status
    extra = 0
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_last_name', 'get_first_name', 'entry_date' , 'exit_date', 'get_is_valid')
    fieldsets = (
        (None, {
            'fields': ('user', 'birth_date')
        }),
        ('Lab Status', {
            'fields': ('entry_date', 'exit_date')
        }),
    )
    inlines = [EmployeeStatusInline]
    list_filter=('entry_date' , 'exit_date')
     
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'
    
    def get_is_valid(self, obj):
        return obj.user.is_active
    get_is_valid.short_description = 'Is Active'
    get_is_valid.admin_order_field = 'user__is_a&ctive'
    get_is_valid.boolean = True
    
class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname' )

# For Team Admin
class TeamMateInline(admin.TabularInline):
    model = TeamMate
    extra=0
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader' )
    inlines = [TeamMateInline]
     
# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(Employee_Status)
admin.site.register(Employee_Type, EmployeeTypeAdmin)

admin.site.register(Team, TeamAdmin)