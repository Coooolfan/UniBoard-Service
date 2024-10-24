from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.note.NoteFile import NoteFile
from api.serializers import NoteFileSerializer


class NoteFileList(APIView):
    queryset = NoteFile.objects.all()
    serializer_class = NoteFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        file_list = request.FILES.getlist('file[]')
        errFiles = []
        succMap = {}
        for file in file_list:
            serializer = NoteFileSerializer(data={'file': file})
            if serializer.is_valid():
                original_filename = file.name
                serializer.save()
                succMap[original_filename] = serializer.instance.file.url
            else:
                errFiles.append(file.name)
        # 返回格式参考 https://ld246.com/article/1549638745630#options-upload
        resp = {
            'msg': '上传成功',
            'code': 0,
            'data': {
                'succMap': succMap,
                'errFiles': errFiles
            }
        }
        return Response(data=resp, status=status.HTTP_201_CREATED)
