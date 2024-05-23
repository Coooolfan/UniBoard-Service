from django.contrib import admin

from api.models import SysInfo


# Register your models here.
@admin.register(SysInfo)
class SysInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')
