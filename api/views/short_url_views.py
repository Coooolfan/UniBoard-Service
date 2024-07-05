import random
import string

import base62 as base
import mmh3
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from UniBoard.settings import SHORT_URL_LENGTH
from api.models import ShortUrl
from api.serializers import ShortUrlSerializer


class ShortUrlList(APIView):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        articles = ShortUrl.objects.all().reverse()
        articles.count()
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 100  # 后台控制显示的最大记录条数

        ret = page.paginate_queryset(articles, request)
        serializer = ShortUrlSerializer(ret, many=True)
        resp = {
            'count': articles.count(),
            'results': serializer.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        long_url = request.data.get('long_url')
        if not long_url:
            return Response(data={'error': 'long_url is required'}, status=status.HTTP_400_BAD_REQUEST)

        short_url = get_short_url(long_url, long_url)

        resp = {
            'short_url': short_url,
            'long_url': long_url
        }
        return Response(data=resp, status=status.HTTP_201_CREATED)


def get_short_url(raw_url, long_url):
    length = SHORT_URL_LENGTH

    _hash = mmh3.hash64(long_url, signed=False)[0]
    base62 = base.encode(_hash)
    base62 = base62[0:length]
    short_url = ShortUrl(
        long_url=raw_url,
        short_url=base62
    )

    try:
        short_url.save()
    except IntegrityError as e:
        return get_short_url(raw_url, long_url + get_random_short_long_url())

    return base62


def get_random_short_long_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
