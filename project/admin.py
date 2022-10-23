from django.contrib import admin
from project.models import Project, Institution, Institution_Participant, Participant

class InstitutionParticipantInLine(admin.TabularInline):
    model=Institution_Participant
    extra=0
    
class ParticipantInLine(admin.TabularInline):
    model=Participant
    extra=0
    
class ProjectAdmin(admin.ModelAdmin):
    inlines = [InstitutionParticipantInLine, ParticipantInLine]
    list_display = ('name', 'start_date', 'end_date', 'status')
    list_filter=('status' ,'start_date', 'end_date')
    
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name')
    
    
# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Institution, InstitutionAdmin)