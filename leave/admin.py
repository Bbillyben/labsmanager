from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Leave_Type, Leave
from .resources import LeaveItemAdminResources
from import_export.admin import ImportExportModelAdmin

class LeaveItemAdmin(ImportExportModelAdmin):
    fields = ('employee','type', 'start_date', 'start_period', 'end_date', 'end_period','comment',)
    list_display = ('employee','type', 'start_date', 'start_period', 'end_date', 'end_period',)
    list_filter = ('employee', 'type', 'start_date', 'end_date','comment')
    resource_classes = [LeaveItemAdminResources]  

# Register your models here.
admin.site.register(Leave_Type)
admin.site.register(Leave, LeaveItemAdmin)