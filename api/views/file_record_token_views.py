import uuid

from django.core.cache import cache
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FileRecord
from api.serializers import FileRecordSerializer


class FileRecordTokenDetail(APIView):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        file_record = FileRecord.objects.get(pk=pk)
        file_record_key = uuid.uuid1().__str__()
        cache_key = "file_record_" + file_record_key
        cache_value = file_record.id
        cache.set(cache_key, cache_value, 5 * 60)
        resp = {
            'file_id': file_record.id,
            'file_name': file_record.file_name,
            'token': file_record_key
        }
        return Response(data=resp, status=status.HTTP_200_OK)
