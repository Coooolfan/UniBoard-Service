import json

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SysInfo
from api.serializers import SysInfoSerializer


class SysInfoList(APIView):
    queryset = SysInfo.objects.all()
    serializer_class = SysInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = SysInfo.objects.all()
        s = SysInfoSerializer(queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        presetSysInfo = ['name', 'version', 'profile', 'avatat', 'contacts']

        s = SysInfoSerializer(data=request.data)
        if not (s.is_valid() and request.data['name'] in presetSysInfo):
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
        if s.is_valid():
            if request.data['name'] == 'contacts' and not contact_check(request.data['value']):
                return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
            s.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class SysInfoDetail(APIView):
    queryset = SysInfo.objects.all()
    serializer_class = SysInfoSerializer
    permission_classes = (permissions.IsAdminUser,)

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

    def put(self, request, pk, format=None):
        try:
            sysinfo = SysInfo.objects.get(pk=pk)
            # 如果是contacts字段，检查是否符合格式
            if sysinfo.name == 'contacts' and not contact_check(request.data['value']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = SysInfoSerializer(sysinfo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SysInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def contact_check(contacts):
    presetContacts = ['telegram', 'qq', 'email', 'github', 'weibo', 'zhihu',
                      'twitter', 'facebook', 'instagram', 'linkedin']
    try:
        contacts = json.loads(contacts)
        for key in contacts:
            if key not in presetContacts:
                return False
        return True
    except json.JSONDecodeError:
        return False
