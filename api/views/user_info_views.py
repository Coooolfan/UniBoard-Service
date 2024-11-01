from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import UserInfo
from api.serializers import UserInfoSerializer


class UserInfoList(APIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    # 游客只能读取，登录用户可以写入
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        queryset = UserInfo.objects.all()
        s = UserInfoSerializer(queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)


class UserInfoDetail(APIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def patch(self, request, pk, format=None):
        try:
            userInfo = UserInfo.objects.get(pk=pk)
            s = UserInfoSerializer(userInfo, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
