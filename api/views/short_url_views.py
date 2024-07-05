import base62 as base
import mmh3
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ShortUrl
from api.serializers import ShortUrlSerializer


class ShortUrlList(APIView):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        long_url = request.data.get('long_url')
        if not long_url:
            return Response(data={'error': 'long_url is required'}, status=status.HTTP_400_BAD_REQUEST)

        hash = mmh3.hash128(long_url)
        base62 = base.encode(hash)
        if base62 is None:
            return Response(data={'error': 'base62 encode error, your long_url is: ' + long_url},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        short_url = ShortUrl.objects.create(long_url=long_url, short_url=base62)
        print(short_url)
        return Response(data="", status=status.HTTP_201_CREATED)
