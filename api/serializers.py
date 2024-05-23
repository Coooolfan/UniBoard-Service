from rest_framework import serializers

from api.models import SysInfo


class SysInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SysInfo
        fields = ['id', 'name', 'value']
