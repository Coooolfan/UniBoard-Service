from django.contrib import admin

from api.models import *


# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'profile', 'avatar', 'contacts', 'slogan', 'banner', 'name_font')
    search_fields = ('name', 'version', 'profile', 'avatar', 'contacts', 'slogan', 'banner', 'name_font')


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'unit', 'desc')
    search_fields = ('name', 'type', 'unit', 'desc')


@admin.register(MonitoredObject)
class MonitoredObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    search_fields = ('name', 'desc')


@admin.register(ObjectMetric)
class ObjectMetricAdmin(admin.ModelAdmin):
    list_display = ('monitored_object_id', 'metric_id')
    search_fields = ('monitored_object_id', 'metric_id')


@admin.register(MetricData)
class MetricDataAdmin(admin.ModelAdmin):
    list_display = ('monitor_object_id', 'insert_time', 'report_time', 'delay', 'data')
    search_fields = ('monitor_object_id', 'insert_time', 'report_time', 'delay', 'data')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'insert_time', 'update_time')
    search_fields = ('title', 'value', 'insert_time', 'update_time')


@admin.register(HyperLink)
class HyperLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'icon', 'color', 'desc')
    search_fields = ('title', 'url', 'icon', 'color', 'desc')


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'short_url', 'gmt_create')
    search_fields = ('long_url', 'short_url', 'gmt_create')


@admin.register(SysConfig)
class SysConfigAdmin(admin.ModelAdmin):
    list_display = ('host', 'TOTP_SECRET_KEY')
    search_fields = ('host', 'TOTP_SECRET_KEY')


@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ('file', 'desc', 'file_name', 'share_code', 'permission', 'password', 'create_time')
    search_fields = ('file', 'desc', 'file_name', 'share_code', 'permission', 'password', 'create_time')
