from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SysConfig
from api.serializers import SysConfigSerializer


class SysConfigList(APIView):
    queryset = SysConfig.objects.all()
    serializer_class = SysConfigSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = SysConfig.objects.all()
        s = SysConfigSerializer(queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)


class SysConfigDetail(APIView):
    queryset = SysConfig.objects.all()
    serializer_class = SysConfigSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk, format=None):
        try:
            sysConfig = SysConfig.objects.get(pk=pk)
            s = SysConfigSerializer(sysConfig, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(s.data)
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        except SysConfig.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
