import random
import string

from rest_framework import serializers

from api.models import *


class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        if 'fields' not in kwargs:
            # Instantiate the superclass normally
            super().__init__(*args, **kwargs)
            return

        fields: tuple = kwargs.get('fields')
        kwargs.pop('fields')
        super().__init__(*args, **kwargs)
        # Drop any fields that are not specified in the `fields` argument.
        allowed = set(fields)
        existing = set(self.fields)
        for field_name in existing - allowed:
            self.fields.pop(field_name)


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'version', 'name', 'profile', 'contacts', 'slogan', 'avatar', 'banner', 'name_font']


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


class NoteSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'value', 'insert_time', 'update_time']


class HyperLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HyperLink
        fields = ['id', 'title', 'url', 'icon', 'color', 'desc']


class HyperLinkCacheSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HyperLinkCache
        fields = ['id', 'finished', 'icon', 'title', 'desc', 'url', 'color']


class ShortUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShortUrl
        fields = ['id', 'long_url', 'short_url', 'gmt_create', 'count']


class SysConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SysConfig
        fields = ['id', 'host']


class FileRecordSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = FileRecord
        fields = ['id', 'file', 'desc', 'share_code', 'file_name', 'permission', 'password', 'create_time', 'count']

    def create(self, validated_data):
        # 在保存对象之前生成share_code
        share_code = self.generate_share_code()
        validated_data['share_code'] = share_code
        return super().create(validated_data)

    def generate_share_code(self):
        # 生成一个6位的随机字符串作为share_code
        share_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        # 确保share_code是唯一的，这里只是一个示例，实际应用中可能需要更复杂的逻辑
        while FileRecord.objects.filter(share_code=share_code).exists():
            share_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        return share_code
