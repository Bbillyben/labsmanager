from django.contrib import admin
from .models import Milestones


class MilestonesAdmin(admin.ModelAdmin):
    list_display = ('get_proj_name', 'name', 'desc', 'deadline_date', 'type', 'quotity', 'status')
    list_filter=('status' ,'deadline_date', 'project')
    
    
    def get_proj_name(self, obj):
        return obj.project.__str__()
    
    
admin.site.register(Milestones, MilestonesAdmin)
