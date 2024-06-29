import binascii
import json
from base64 import b64decode

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from UniBoard.settings import DEBUG
from api.models import SysInfo
from api.serializers import SysInfoSerializer


class SysInfoList(APIView):
    queryset = SysInfo.objects.all()
    serializer_class = SysInfoSerializer
    # 游客只能读取，登录用户可以写入
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        queryset = SysInfo.objects.all()
        s = SysInfoSerializer(queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # 新增系统信息，只有DEBUG为True时才能新增，生产环境编辑此表应当使用SysInfoDetail的put方法
        if not DEBUG:
            return Response(status=status.HTTP_403_FORBIDDEN)
        s = SysInfoSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class SysInfoDetail(APIView):
    queryset = SysInfo.objects.all()
    serializer_class = SysInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, format=None):
        try:
            sysinfo = SysInfo.objects.get(pk=pk)
            serializer = SysInfoSerializer(sysinfo)
            return Response(serializer.data)
        except SysInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            sysinfo = SysInfo.objects.get(pk=pk)
            sysinfo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SysInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # 修改系统信息
    def patch(self, request, pk, format=None):
        try:
            sysinfo = SysInfo.objects.get(pk=pk)
            s = SysInfoSerializer(sysinfo, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
        except SysInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def contact_check(contacts):
    presetContacts = ['telegram', 'qq', 'email', 'github', 'weibo', 'zhihu',
                      'twitter', 'facebook', 'instagram', 'linkedin']
    try:
        contacts = json.loads(contacts)
        # demo
        # {"telegram": "telegram", "qq": "qq", "email": "email", "github": "github", "weibo": "weibo",}
        for key in contacts:
            if key not in presetContacts:
                return False
        return True
    except json.JSONDecodeError:
        return False


def link_check(links):
    items = ['icon', 'title', 'desc', 'url', 'color']
    print(links)
    try:
        links = b64decode(links).decode('utf-8')
        links = json.loads(links)
        print("这是一个json")
        # demo
        # [{icon: 'icon', title: 'title', desc: 'desc', url: 'url', color: 'color'}, ...]
        for link in links:
            for item in items:
                if item not in link:
                    return False
        return True
    except json.JSONDecodeError:
        print('json.JSONDecodeError')
        return False
    except binascii.Error:
        print('binascii.Error')
        return False
