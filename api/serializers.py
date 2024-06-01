from rest_framework import serializers

from api.models import *


class SysInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SysInfo
        fields = ['id', 'name', 'value']


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'name', 'type', 'unit', 'desc']


class MonitoredObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonitoredObject
        fields = ['id', 'name', 'desc']


class ObjectMetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ObjectMetric
        fields = ['id', 'monitored_object_id', 'metric_id']


class MetricDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricData
        fields = ['id', 'monitor_object_id', 'insert_time', 'report_time', 'delay', 'data']


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'value', 'insert_time', 'update_time']
