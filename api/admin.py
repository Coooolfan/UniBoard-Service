from django.contrib import admin

from api.models import *


# Register your models here.
@admin.register(SysInfo)
class SysInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')


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
