from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView

from UniBoard.settings import DEBUG
from api.models import FileRecord
from api.serializers import FileRecordSerializer


class FileRecordRedirect(APIView):
    queryset = FileRecord.objects.all()
    serializer_class = FileRecordSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk, filename=None, format=None):
        # 对于直链，可以通过临时token直接下载文件，不需要鉴权
        if not pk.isdigit():
            file_id = cache.get("file_record_" + pk)
            if file_id is None:
                return HttpResponse(status=404)
            return response_file(file_id)

        # 对于超级用户，可以直接通过文件id或者临时token直接下载文件
        if request.user.is_superuser:
            return response_file(int(pk))
        # 对于游客，需要检查文件权限
        else:
            if not pk.isdigit():
                return HttpResponse(status=404)
            try:
                file_record = FileRecord.objects.get(pk=pk)
            except FileRecord.DoesNotExist:
                return HttpResponse(status=404)
            # 私有文件只能被超级用户下载
            if file_record.permission == FileRecord.Permission.PRIVATE.value:
                return HttpResponse(status=404)
            # 公共文件可以直接下载
            elif file_record.permission == FileRecord.Permission.PUBLIC.value:
                return response_file(int(pk))
            # 需要密码的文件需要提供密码
            else:
                password = request.query_params.get('pw')
                if password is None or password != file_record.password:
                    return HttpResponse(status=401)
                return response_file(int(pk))


def get_file(file_id: int):
    file_record = FileRecord.objects.get(pk=file_id)
    file_record.file.open()
    file = file_record.file.read()
    file_record.file.close()
    return file


def response_file(file_id: int):
    # 通过django的HttpResponse返回文件
    if DEBUG:
        file = get_file(file_id)
        # 更新文件下载次数，原子化操作，防止并发问题
        FileRecord.objects.filter(pk=file_id).update(count=F('count') + 1)
        return HttpResponse(file, content_type='application/octet-stream')
    else:
        # 线上环境使用nginx返回，重定向到/protected/路径下
        file_record = FileRecord.objects.get(pk=file_id)
        # 更新文件下载次数，原子化操作，防止并发问题
        FileRecord.objects.filter(pk=file_id).update(count=F('count') + 1)
        file_path = file_record.file
        response = HttpResponse()
        del response['Content-Type']
        response['X-Accel-Redirect'] = ('/protected/' + str(file_path)).encode('utf-8')
        response['Content-Disposition'] = 'attachment; filename=' + file_record.file_name
        return response
