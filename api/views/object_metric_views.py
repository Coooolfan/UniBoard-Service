from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ObjectMetric
from api.serializers import ObjectMetricSerializer


class ObjectMetricList(APIView):
    queryset = ObjectMetric.objects.all()
    serializer_class = ObjectMetricSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        object_metrics = ObjectMetric.objects.all()
        serializer = ObjectMetricSerializer(object_metrics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ObjectMetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectMetricDetail(APIView):
    queryset = ObjectMetric.objects.all()
    serializer_class = ObjectMetricSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ObjectMetric.objects.get(pk=pk)
        except ObjectMetric.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        object_metric = self.get_object(pk)
        if object_metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ObjectMetricSerializer(object_metric)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        object_metric = self.get_object(pk)
        if object_metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ObjectMetricSerializer(object_metric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        object_metric = self.get_object(pk)
        if object_metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object_metric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
