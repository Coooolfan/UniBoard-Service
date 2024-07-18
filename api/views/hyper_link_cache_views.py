import base64
import logging
import mimetypes

from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from UniBoard.settings import MEDIA_ROOT
from api.models import HyperLinkCache
from api.serializers import HyperLinkCacheSerializer
from api.tasks import fetch_page_info_task

logger = logging.getLogger(__name__)


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
        if not hyper_link_cache.finished:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HyperLinkCacheSerializer(hyper_link_cache)
        hyper_link_cache_base64 = serializer.data
        hyper_link_cache_base64['icon'] = icon_to_base64(hyper_link_cache_base64["icon"])
        return Response(hyper_link_cache_base64, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk, format=None):
        hyper_link_cache = HyperLinkCache.objects.get(pk=pk)
        serializer = HyperLinkCacheSerializer(hyper_link_cache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def icon_to_base64(url):
    url = MEDIA_ROOT + '/' + url[7:]
    try:
        # 从文件路径获取Byte
        with open(url, "rb") as f:
            response = f.read()
        # 猜测MIME类型
        mime_type = mimetypes.guess_type(url)[0]
        # 将获取的内容转换为base64编码
        content_base64 = base64.b64encode(response)
        # 将base64编码的内容转换为字符串
        content_base64_str = content_base64.decode('utf-8')
        # 生成完整的base64编码的图片URL
        full_base64_str = f"data:{mime_type};base64,{content_base64_str}"
    except Exception as e:
        # 如果出现异常，返回None
        logger.error(f"Error converting URL to base64: {str(e)}")
        full_base64_str = ""
    return full_base64_str
