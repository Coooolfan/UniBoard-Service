from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from UniBoard.settings import DEBUG
from api.models import FileRecord
from api.serializers import FileRecordSerializer


class FileRecordRedirect(APIView):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk: str, filename=None, format=None):
        # 对于直链(由UUID构成，包含短横线)，可以通过临时token直接下载文件，不需要鉴权
        if '-' in pk:
            file_id = cache.get("file_record_" + pk)
            if file_id is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return response_file(str(file_id))

        # 对于share_code，需要检查文件权限
        if request.user.is_superuser:
            # 对于超级用户，可以直接通过文件id或者临时token直接下载文件
            return response_file(pk)
        else:
            # 对于游客，需要检查文件权限
            try:
                file_record = get_file_record(pk)
            except FileRecord.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            # 私有文件只能被超级用户下载
            if file_record.permission == FileRecord.Permission.PRIVATE.value:
                return Response(status=status.HTTP_404_NOT_FOUND)
            # 公共文件可以直接下载
            elif file_record.permission == FileRecord.Permission.PUBLIC.value:
                return response_file(pk)
            # 需要密码的文件需要提供密码
            else:
                password = request.query_params.get('pw')
                if password is None or password != file_record.password:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                return response_file(pk)


def response_file(key: str):
    file_record = get_file_record(key)
    # 通过django的HttpResponse返回文件
    if DEBUG:
        file_record.file.open()
        file = file_record.file.read()
        file_record.file.close()
        # 更新文件下载次数，原子化操作，防止并发问题
        FileRecord.objects.filter(pk=file_record.id).update(count=F('count') + 1)
        return HttpResponse(file, content_type='application/octet-stream')
    else:
        # 线上环境使用nginx返回，重定向到/protected/路径下
        # 更新文件下载次数，原子化操作，防止并发问题
        FileRecord.objects.filter(pk=file_record.id).update(count=F('count') + 1)
        response = HttpResponse()
        del response['Content-Type']
        response['X-Accel-Redirect'] = '/protected/' + str(file_record.file)
        response['Content-Disposition'] = 'attachment; filename=' + file_record.file_name
        return response


def get_file_record(key: str) -> FileRecord:
    if key.isdigit():
        file_record = FileRecord.objects.get(pk=key)
    else:
        file_record = FileRecord.objects.get(share_code=key)
    return file_record
