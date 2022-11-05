from django.contrib import admin
from .models import LMUserSetting


class LMUserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'key','value',)
    list_filter=('user' , 'key')
# Register your models here.
admin.site.register(LMUserSetting, LMUserSettingAdmin)
