from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import HyperLink
from api.serializers import HyperLinkSerializer


class HyperLinkList(APIView):
    queryset = HyperLink.objects.all()
    serializer_class = HyperLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        hyper_links = HyperLink.objects.all()
        serializer = HyperLinkSerializer(hyper_links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = HyperLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HyperLinkDetail(APIView):
    queryset = HyperLink.objects.all()
    serializer_class = HyperLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return HyperLink.objects.get(pk=pk)
        except HyperLink.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        hyper_link = self.get_object(pk)
        if hyper_link is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HyperLinkSerializer(hyper_link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        hyper_link = self.get_object(pk)
        if hyper_link is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HyperLinkSerializer(hyper_link, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        hyper_link = self.get_object(pk)
        if hyper_link is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hyper_link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
