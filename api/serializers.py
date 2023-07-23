from rest_framework import serializers
from .models import TrustedDevice, MonitoredObjects, Status


class MonitoredObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoredObjects
        fields = ('objectID', 'objectName', 'category', 'statusList')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('statusID', 'objectID', 'insertStamp', 'repotyStamp', 'status')


class TrustedDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedDevice
        fields = ('deviceID',)
