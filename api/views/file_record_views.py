from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FileRecord
from api.serializers import FileRecordSerializer


class FileRecordList(APIView):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = FileRecord.objects.all().order_by('create_time')

        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 100  # 后台控制显示的最大记录条数

        ret = page.paginate_queryset(queryset, request)
        serializer = FileRecordSerializer(ret, many=True)
        resp = {
            'count': queryset.count(),
            'results': serializer.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # 上传文件，文件的share_code是自动生成，参见FileRecordSerializer的create方法
        s = FileRecordSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class FileRecordDetail(APIView):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 此接口只会从文件分享页发起
    def get(self, request, pk, format=None):
        try:
            file_record = FileRecord.objects.get(share_code=pk)
        except FileRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if file_record.permission == FileRecord.Permission.PRIVATE.value and not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = FileRecordSerializer(file_record, fields=('file', 'file_name', 'create_time', 'permission', 'desc'))
        return Response(data=s.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        file_record = FileRecord.objects.get(pk=pk)
        s = FileRecordSerializer(file_record, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file_record = FileRecord.objects.get(pk=pk)
        file_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
