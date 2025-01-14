import random
import string
import uuid

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
        fields = ['id', 'name', 'profile', 'contacts', 'slogan', 'avatar', 'banner', 'name_font']


class NoteSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'value', 'insert_time', 'update_time']


class NoteFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NoteFile
        fields = ['id', 'file', 'insert_time', 'update_time']

    def create(self, validated_data):
        file = validated_data['file']
        if file:
            new_filename = str(uuid.uuid4())
            file.name = new_filename + file.name[file.name.rfind('.'):]
        return super().create(validated_data)


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
        fields = ['id', 'host', 'show_copyright', "show_profile_page"]


class FileRecordSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = FileRecord
        fields = ['id', 'file', 'desc', 'share_code', 'file_name', 'permission', 'password', 'create_time', 'count']

    def create(self, validated_data):
        # 在保存对象之前生成share_code
        share_code = generate_filerecord_share_code()
        validated_data['share_code'] = share_code
        file = validated_data['file']
        if file:
            new_filename = str(uuid.uuid4())
            file.name = new_filename
        return super().create(validated_data)


def generate_filerecord_share_code():
    # 生成一个6位的随机字符串作为share_code
    share_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    # 确保share_code是唯一的
    while FileRecord.objects.filter(share_code=share_code).exists():
        share_code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return share_code
