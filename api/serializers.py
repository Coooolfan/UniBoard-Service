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
