from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import HyperLinkCache
from api.serializers import HyperLinkCacheSerializer
from api.tasks import fetch_page_info_task


class HyperLinkCacheList(APIView):
    queryset = HyperLinkCache.objects.all()
    serializer_class = HyperLinkCacheSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request: Request, format=None):
        # 只需要接受一个url参数
        url = request.data.get('url')
        if url is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # new一个HyperLinkCache对象
        new_hyper_link_cache = HyperLinkCache(
            finished=False,
            icon=None,
            title="New HyperLink",
            desc="New HyperLink Desc",
            url=url,
            color="#f2f2f2"
        )
        # 保存到数据库并返回ID
        new_hyper_link_cache.save()
        fetch_page_info_task.delay(new_hyper_link_cache.id)
        return Response(data={"id": new_hyper_link_cache.id}, status=status.HTTP_201_CREATED)


class HyperLinkCacheDetail(APIView):
    queryset = HyperLinkCache.objects.all()
    serializer_class = HyperLinkCacheSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request: Request, pk, format=None):
        hyper_link_cache = HyperLinkCache.objects.get(pk=pk)
        serializer = HyperLinkCacheSerializer(hyper_link_cache)
        return Response(serializer.data)

    def patch(self, request: Request, pk, format=None):
        hyper_link_cache = HyperLinkCache.objects.get(pk=pk)
        serializer = HyperLinkCacheSerializer(hyper_link_cache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
