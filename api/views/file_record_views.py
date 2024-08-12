from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.models import FileRecord
from api.serializers import FileRecordSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class FileRecordList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = FileRecord.objects.all().order_by('create_time')
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})


class FileRecordDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin,
                       DestroyModelMixin):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'pk'

    # 此接口只会从文件分享页发起
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None or instance.permission == FileRecord.Permission.PRIVATE.value:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, fields=('file', 'file_name', 'create_time', 'permission', 'desc'))
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(share_code=self.kwargs[self.lookup_field])
        except FileRecord.DoesNotExist:
            return None
        self.check_object_permissions(self.request, obj)
        return obj
